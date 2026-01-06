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

        vpc = ec2.Vpc(
            self, f"PortalEntidadesVpc-{stage}",
            max_azs=1,
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"PrivateSubnet-{stage}",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=f"PublicSubnet-{stage}",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )
        
        vpc.add_interface_endpoint(
            f"SecretsManagerEndpoint-{stage}",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER
        )
        

        creds = rds.Credentials.from_generated_secret("app_user", secret_name=f"/pe_mss/aurora/{stage}/credentials")
        
        db_name = "PortalEntidades_UserTable"

        self.cluster = rds.DatabaseCluster(
            self, f"AuroraSrvls-{stage}",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_16_8
            ),
            writer=rds.ClusterInstance.serverless_v2(
                "WriterInstance",
                scale_with_writer=True,
            ),
            readers=[
                rds.ClusterInstance.serverless_v2(
                    "ReaderInstance",
                    scale_with_writer=True,
                )
            ] if stage == "PROD" else [],
            serverless_v2_min_capacity=0,
            serverless_v2_max_capacity=2,
            default_database_name=db_name,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            credentials=creds,
            removal_policy=removal,
            enable_data_api=True,
            backup=rds.BackupProps(
                retention=Duration.days(7 if stage != "PROD" else 30)
            ),
        )

        self.secret = self.cluster.secret 
        self.default_database_name = db_name
        self.vpc = vpc