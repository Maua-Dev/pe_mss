import base64
import io
import pandas as pd
import urllib3
import os
import json

from src.shared.clients.s3_client import S3Client
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
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

    def __call__(self, file_base64: str, requester_user_id: User, auth_token: str) -> list[User]:

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
        
        uploaded_user = []
        for _, row in df.iterrows():
            user_data = {
                'name': row['name'],
                'email': row['email'],
                'organization': row['organization'],
                'role': row['role'],
                'state': row['state']
            }
            
            uploaded_user.append(user_data)
            
        payload = {
            'new_user': [
                dict(user_data) for user_data in uploaded_user
            ]
        }
        
        json_body = json.dumps(payload).encode('utf-8')

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
        duplicated_users = []
        
        if response.status == 400 and "alredy exists" in response_text:
            # NO FUTURO IMPLEMENTAR A CAPTURA DE VÁRIOS USUÁRIOS DUPLICADOS
            duplicated_users.append({
                "message": response_text
            })
        
        # Se for outro tipo de erro (não duplicado), levanta exceção
        elif response.status == 400 or response.status == 500:
            raise EntityError(f"Error from create_user endpoint: {response_text}")
        
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            raise EntityError("Failed to decode JSON response from create_user endpoint.")
        
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
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='auto') as writer:
                combined_df.to_excel(writer, index=False)
            output.seek(0)
            self.s3_client.upload_planilha_geral_excel(file_content=output.getvalue())
        
        if isinstance(response_data, list):
            return response_data
        
        elif isinstance(response_data, dict):
            return list(response_data.get("data"))
        
        else:
            raise EntityError(f"Unexpected response format from API: {type(response_data)}")