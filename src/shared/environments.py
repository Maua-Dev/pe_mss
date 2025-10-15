import enum
from enum import Enum
import os
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str
    region: str
    endpoint_url: str = None
    dynamo_endpoint_url: str = None
    dynamo_endpoint_port: str = None
    dynamo_region: str = None
    db_name: str
    db_local_user: str
    db_local_pass: str
    db_local_host: str
    db_local_port: str
    db_cluster_arn: str
    db_secret_arn: str
    cloud_frontget_user_presenter_distribution_domain: str
    mss_name: str 
    graph_microsoft_endpoint: str

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        self.mss_name = os.environ.get("MSS_NAME")
        
        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "portalentidadesstackd-portalentidadesbackbucket-sheet"
            self.region = "us-east-1"
            self.endpoint_url = "http://localhost:8000"
            self.db_name = os.environ.get("POSTGRES_LOCAL_DB", "mydatabase")
            self.db_local_user = os.environ.get("POSTGRES_LOCAL_USER", "myuser")
            self.db_local_pass = os.environ.get("POSTGRES_LOCAL_PASS", "mypassword")
            self.db_local_host = os.environ.get("POSTGRES_LOCAL_HOST", "localhost")
            self.db_local_port = os.environ.get("POSTGRES_LOCAL_PORT", "5432")
            self.dynamo_endpoint_url = os.environ.get("DYNAMO_ENDPOINT_URL", "http://localhost")
            self.dynamo_endpoint_port = os.environ.get("DYNAMO_ENDPOINT_PORT", "8000")
            self.dynamo_region = os.environ.get("DYNAMO_REGION", "local")
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"
            self.bucket_endpoint_url = "http://localhost:9000"
            self.graph_microsoft_endpoint = "https://graph.microsoft.com"

        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.region = os.environ.get("REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.db_cluster_arn = os.environ.get("DB_CLUSTER_ARN")
            self.db_secret_arn = os.environ.get("DB_SECRET_ARN")
            self.db_name = os.environ.get("DB_NAME")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")
            self.graph_microsoft_endpoint = os.environ.get("GRAPH_MICROSOFT_ENDPOINT")

    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            # from src.shared.infra.repositories.user_repository_postgres import UserRepositoryPostgres
            # from src.shared.infra.external.postgres.datasources.postgres_datasource import RdsDataDatasource
            return UserRepositoryMock
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_observability() -> IObservability:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.external.observability.observability_mock import ObservabilityMock
            return ObservabilityMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
            return ObservabilityAWS
        else:
            raise Exception("No observability class found for this stage")
    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

