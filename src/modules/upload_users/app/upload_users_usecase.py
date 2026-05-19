import base64
import binascii
import io
import re
import uuid
import pandas as pd
import os

from src.shared.clients.s3_client import S3Client
from src.shared.domain.entities.user import User
from src.shared.domain.enums.active_enum import ACTIVE
from src.shared.domain.enums.organization_enum import ORGANIZATION
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.state_enum import STATE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.enums.role_enum import ROLE

class UploadUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.stage = (os.environ.get("STAGE") or "TEST").upper()
        
        if self.stage == "TEST":
            self.s3_client = S3Client("bucket-test-pe")
        else:
            self.s3_client = S3Client(os.environ.get("S3_BUCKET_NAME"))

    def __call__(self, file_base64: str, requester_user_id: str) -> tuple[list[dict], list[dict]]:
        
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

            # novo catch de erro de conversao 
            try:
                file_bytes = base64.b64decode(file_base64)
            except binascii.Error as error:
                raise error

            try:
                df = pd.read_excel(io.BytesIO(file_bytes))
            except Exception as error:
                raise EntityError(f"Invalid file content: {str(error)}")
            
            # WARNING: Validar as colunas
            expected_columns = ['name', 'email', 'role', 'organization', 'state']
            if not all(column in df.columns for column in expected_columns):
                raise EntityError("Invalid file format. Expected columns: " + ", ".join(expected_columns))
            
            # essa lógica segue a mesma da validação de usuários na criação de usuários (create_user_usecase.py)
            for _, row in df.iterrows():
                user_data = {
                    'name': row.get('name'),
                    'email': row.get('email'),
                    'organization': row.get('organization'),
                    'role': row.get('role'),
                    'state': row.get('state')
                }
                
                for key, value in user_data.items():
                    if pd.isna(value):
                        user_data[key] = None

                email = user_data.get("email")
                try:
                    self.repo.get_user_by_email(email)
                    duplicated_users.append({
                        "name": user_data.get("name"),
                        "email": email,
                        "organization": user_data.get("organization"),
                        "role": user_data.get("role"),
                        "state": user_data.get("state")
                    })
                    continue
                except NoItemsFound:
                    pass

                try:
                    user = User(
                        user_id=f"{uuid.uuid4()}",
                        name=user_data.get("name"),
                        email=email,
                        role=ROLE(user_data.get("role")),
                        organization=ORGANIZATION(user_data.get("organization")),
                        active=ACTIVE.ACTIVE,
                        state=STATE(user_data.get("state")) if user_data.get("state") else STATE.PENDING,
                        ra=re.search(r"(.+)@", email).group(1)
                    )
                except Exception as error:
                    raise EntityError(f"Invalid user data for {email}: {str(error)}")

                self.repo.has_permission_target_user(requester_id=requester_user_id, target_user=user)
                created_user = self.repo.create_user(new_user=user)

                created_users.append({
                    "name": created_user.name,
                    "email": created_user.email,
                    "organization": created_user.organization.value if created_user.organization else None,
                    "role": created_user.role.value if created_user.role else None,
                    "state": created_user.state.value if created_user.state else None
                })
                
            # breakpoint, em env teste (pytest) nao temos o bucket sem ser pelo MinIO
            # se quiser rodar localmente com o MinIO mude seu STAGE para algo diferente de TEST, DEV, HOMOLOG, PROD
            if self.stage == "TEST":
                return created_users, duplicated_users

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