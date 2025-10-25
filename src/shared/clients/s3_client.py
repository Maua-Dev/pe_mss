import boto3
import botocore
import datetime
from botocore.exceptions import ClientError

from src.shared.environments import Environments


class S3Client:
    
    bucket_name: str
    prefix_key_org: str
    prefix_key_general: str
    excel_extension: str

    def __init__(self, bucket_name: str):
        
        self.prefix_key_general = "/planilhas/geral/"
        self.prefix_key_org = "/planilhas/org/"
        self.excel_extension = "xlsx"
        self.bucket_name = bucket_name
        
        self.__envs = Environments.get_envs()
        stage = self.__envs.stage.value
        if stage == "TEST":
            # configuracao pro MINIO (bucket local simulado tipo dynamo pelo docker)
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=self.__envs.client_id,
                aws_secret_access_key=self.__envs.client_secret,
                endpoint_url=self.__envs.bucket_endpoint_url,
                region_name=self.__envs.region,
                config=boto3.session.Config(signature_version="s3v4"),
            )
        else:
            self.s3 = boto3.client("s3")
            
    def formata_caminho(self, file_type: str, org: str = None) -> str:
        
        agora = datetime.datetime.now()
        ano = agora.year
        semestre = "01" if agora.month <= 6 else "02"
        
        if not file_type:
            
            return ""
        
        if org:
            
            return self.prefix_key_org + f"planilha_{org}_{ano}_{semestre}.{file_type}"
        
        else:
            
            return self.prefix_key_general + f"planilha_geral_{ano}_{semestre}.{file_type}"
        
            
    def upload_planilha_geral_excel(self, file_content: bytes) -> dict:
        
        key = self.formata_caminho(file_type=self.excel_extension)
                
        try:
            response = self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_content
                # Metadata={
                #     'upload-source': 'meu-app'
                # }
            )
            
            return response

        except Exception as e:
            raise e
            
    def upload_planilha_org_excel(self, org: str, file_content: bytes) -> dict:
        
        key = self.formata_caminho(org=org, file_type=self.excel_extension)
            
        try:
            response = self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_content
                # Metadata={
                #     'upload-source': 'meu-app'
                # }
            )
            
            return response

        except Exception as e:
            raise e
    
    def retreive_planilha_geral(self) -> tuple[bytes | None, dict]:
        
        key = self.formata_caminho(file_type=self.excel_extension)
        
        try:
            
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            
            object_content = response["Body"].read()
            
            metadata = response
            del metadata['Body']
            
            return object_content, metadata
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"Erro: O objeto com a chave '{key}' não foi encontrado no bucket '{self.bucket_name}'.")
            else:
                print(f"Um erro do cliente AWS ocorreu: {e}")
            return None, {"error": str(e)}
        
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            return None, {"error": str(e)}
            
    def retreive_planilha_org(self, org: str) -> tuple[bytes | None, dict]:
        
        key = self.formata_caminho(org=org, file_type=self.excel_extension)
        
        try:
            
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            
            object_content = response["Body"].read()
            
            metadata = response
            del metadata['Body']
            
            return object_content, metadata
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"Erro: O objeto com a chave '{key}' não foi encontrado no bucket '{self.bucket_name}'.")
            else:
                print(f"Um erro do cliente AWS ocorreu: {e}")
            return None, {"error": str(e)}
        
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            return None, {"error": str(e)}
             
    def check_exists(self, key) -> bool:
        
        try:
            
            self.s3.head_object(
                Bucket=self.bucket_name,
                key=key
            )
            
            return True
            
        except botocore.exceptions.ClientError as e:
            
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                print("Erro do cliente")
                raise e
