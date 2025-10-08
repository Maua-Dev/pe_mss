import boto3
import botocore

from src.shared.environments import Environments


class s3_client:
    
    bucket_name: str
    prefix_key_org: str
    prefix_key_general: str

    def __init__(self, bucket_name: str):
        
        self.prefix_key_general = "/planilhas/geral/"
        self.prefix_key_org = "/planilhas/org/"
        
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
            
    def upload_planilha_org(self, org: str, file: bytes) -> dict:
        pass
    
    def retreive_planilha_geral(self) -> dict:
        pass
    
    def retreive_planilha_org(self) -> dict:
        pass
             
    def check_exists(self, key: str) -> bool:
        
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
