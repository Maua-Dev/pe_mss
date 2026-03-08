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
            max_azs=2,
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"PrivateSubnet-{stage}",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )
        
        single_az_selection = ec2.SubnetSelection(
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            availability_zones=[vpc.availability_zones[0]] 
        )
        
        vpc.add_interface_endpoint(
            f"SecretsManagerEndpoint-{stage}",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=single_az_selection
        )
        
        vpc.add_interface_endpoint(
            f"RdsDataEndpoint-{stage}",
            service=ec2.InterfaceVpcEndpointAwsService.RDS_DATA,
            subnets=single_az_selection
        )
        
        creds = rds.Credentials.from_generated_secret("app_user", secret_name=f"/pe_mss/aurora/{stage}/credentials")
        
        db_name = "PortalEntidades_UserTable"

        aurora_paramter_group= rds.ParameterGroup(
            self,
            f"AuroraPgCronParamGroup-{stage}",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_16_8
            ),
            description= "paramter group que habilita o pg_cron",
            paramter={
                "shared_preload_libraries": "pg_stat_statements, pg_cron",
                "cron.database_name": db_name
            }
        )

        self.cluster = rds.DatabaseCluster(
            self, f"AuroraSrvls-{stage}",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_16_8
            ),
            writer=rds.ClusterInstance.serverless_v2(
                "WriterInstance",
                scale_with_writer=True,
            ),
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
                retention=Duration.days(5)
            ),
            parameter_group=aurora_paramter_group
        )

        self.secret = self.cluster.secret 
        self.default_database_name = db_name
        self.vpc = vpc