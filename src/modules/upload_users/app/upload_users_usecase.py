import base64
import io
import uuid
import pandas as pd
import urllib3
import os
import json

from src.shared.clients.s3_client import S3Client
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.domain.enums.role_enum import ROLE

class UploadUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
        
        if os.environ.get("STAGE") == "TEST":
            self.s3_client = S3Client("bucket-test-pe")
        else:
            self.s3_client = S3Client(os.environ.get("S3_BUCKET_NAME"))
            
        self.http_client = urllib3.PoolManager()

    def __call__(self, file_base64: str, requester_user_id: User, auth_token: str) -> tuple[list[dict], list[dict]]:
        
        created_users = []
        duplicated_users = []

        try:
            if type(file_base64) != str:
                raise EntityError("file_base64")
            
            if type(requester_user_id) != str:
                raise EntityError("requester_user_id")

            requester_user = self.repo.get_user(user_id=requester_user_id)
            if requester_user.role != ROLE.PRESIDENT:
                raise PermissionError("Only users with PRESIDENT role can upload users.")

            file_bytes = base64.b64decode(file_base64)
            df = pd.read_excel(io.BytesIO(file_bytes))
            
            # WARNING: Validar as colunas
            expected_columns = ['name', 'email', 'role', 'organization', 'state']
            if not all(column in df.columns for column in expected_columns):
                raise EntityError("Invalid file format. Expected columns: " + ", ".join(expected_columns))
            
            for _, row in df.iterrows():
                user_data = {
                    'name': row['name'],
                    'email': row['email'],
                    'organization': row['organization'],
                    'role': row['role'],
                    'state': row['state']
                }
                
                payload = {
                    'new_user': [user_data]
                }
                
                json_body = json.dumps(payload).encode('utf-8')
                
                if not os.environ.get("STAGE") == "TEST":
                    
                    #this will only work in aws, here we will only test for minio bucket

                    response = self.http_client.request(
                        "POST", 
                        os.environ.get("CREATE_USER_ENDPOINT"), 
                        body=json_body,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"{auth_token}" #Already has Bearer prefix
                        }
                    )
                
                    response_text = response.data.decode('utf-8')
                
                    if response.status == 201 or response.status == 200:
                        try:
                            response_data = json.loads(response_text)
                            if response_data.get("users"):
                                #caso lista de usuários (não é pra acontecer)
                                created_users.append(response_data["users"][0]["user"])
                            elif response_data.get("user"):
                                #caso usuário único
                                created_users.append(response_data["user"])
                            else:
                                created_users.append(user_data)
                        except:
                            created_users.append(user_data)

                    elif response.status == 400 and "alredy exists" in response_text:
                        duplicated_users.append(user_data)
                    
                    else:
                        raise EntityError(f"Error from create_user endpoint for user {user_data.get('email')}: {response_text}")

                else:
                    
                    # LOGIC FOR TESTING WITH MOCK REPO
                    try:
                                                
                        for existing_user in self.repo.users:
                            if existing_user.email == user_data['email']:
                                raise DuplicatedItem(f"User with email {user_data['email']} already exists.")
                            
                        created_users.append(user_data)
                        
                    except DuplicatedItem:
                        duplicated_users.append(user_data)
                        continue
                
            # Adicionar na planilha da org
            org_spreadsheet, error = self.s3_client.retreive_planilha_org(org=requester_user.organization)
            if error.get("error"):
                # Caso não exista, criar
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='auto') as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)
                self.s3_client.upload_planilha_org_excel(org=requester_user.organization, file_content=output.getvalue())
            else:
                existing_df = pd.read_excel(io.BytesIO(org_spreadsheet))
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=['email'], keep='first')
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='auto') as writer:
                    combined_df.to_excel(writer, index=False)
                output.seek(0)
                self.s3_client.upload_planilha_org_excel(org=requester_user.organization, file_content=output.getvalue())
                
            # Adicionar na planilha geral
            general_spreadsheet, error = self.s3_client.retreive_planilha_geral()

            if error.get("error"):
                # Caso não exista, criar a planilha xlsx a partir do dataframe
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='auto') as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)
                self.s3_client.upload_planilha_geral_excel(file_content=output.getvalue())
            else:
                existing_df = pd.read_excel(io.BytesIO(general_spreadsheet))
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=['email'], keep='first')
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='auto') as writer:
                    combined_df.to_excel(writer, index=False)
                output.seek(0)
                self.s3_client.upload_planilha_geral_excel(file_content=output.getvalue())
            
            return created_users, duplicated_users

        except Exception as e:
            # Rollback logic to be implemented if necessary !!!! (quem for trabalhar futuramente aqui por favor crie um jeito eficiente e bom de dar rollback 🐉)
            print(f"Rollback triggered due to: {str(e)}")
            raise e