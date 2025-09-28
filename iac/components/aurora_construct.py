# iac/contructs/aurora_construct.py
from aws_cdk import (
    RemovalPolicy, Duration,
    aws_ec2 as ec2,
    aws_rds as rds,
)
from constructs import Construct
import os

class AuroraConstruct(Construct):
    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)

        github_ref_name = (os.environ.get("GITHUB_REF_NAME") or "").lower()
        if "prod" in github_ref_name:
            stage, removal = "PROD", RemovalPolicy.RETAIN
        elif "homolog" in github_ref_name:
            stage, removal = "HOMOLOG", RemovalPolicy.RETAIN
        else:
            stage, removal = "DEV", RemovalPolicy.DESTROY

        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        creds = rds.Credentials.from_generated_secret("app_user", secret_name=f"/pe_mss/aurora/{stage}/credentials")

        self.cluster = rds.ServerlessCluster(
            self, f"AuroraSrvls-{stage}",
            engine=rds.DatabaseClusterEngine.AURORA_POSTGRESQL,
            default_database_name="PortalEntidades_UserTable",
            vpc=vpc,
            enable_data_api=True,                      
            credentials=creds,
            scaling=rds.ServerlessScalingOptions(
                auto_pause=Duration.minutes(10),       
                min_capacity=rds.AuroraCapacityUnit.ACU_2,
                max_capacity=rds.AuroraCapacityUnit.ACU_8,
            ),
            removal_policy=removal,
        )

        self.secret = self.cluster.secret 
