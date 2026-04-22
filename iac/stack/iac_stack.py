from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam,
    Aws
)


from constructs import Construct
# Aqui não precisamos importar subindo um diretório pois a execução acontece diretamente do diretório iac
from components.aurora_construct import AuroraConstruct
from components.lambda_construct import LambdaConstruct
from components.s3_construct import S3Construct
from components.dynamo_construct import DynamoConstruct
from components.sm_construct import SmConstruct
from components.ssm_construct import SsmConstruct
from components.apigw_construct import ApigwConstruct
import os

class IacStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        stack_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ) -> None:
        
        super().__init__(scope, stack_id, **kwargs)

        stage = stage.lower()

        self.apigw_construct = ApigwConstruct(
            self,
            construct_id="Apigw",
            stack_name=stack_name,
            stage=stage
        )
        
        self.dynamo_construct = DynamoConstruct(
            self, 
            construct_id="Dynamo",
            stack_name=stack_name,
            stage=stage
        )

        self.aurora_construct = AuroraConstruct(
            self, 
            construct_id="Aurora",
            stack_name=stack_name,
            stage=stage
        )
        
        self.s3_construct = S3Construct(
            self,
            construct_id="S3",
            stack_name=stack_name,
            stage=stage
        )
        
        self.ssm_construct = SsmConstruct(
            self,
            construct_id="SystemsManager",
            stack_name=stack_name,
            stage=stage,
            mss_name_identification_for_path="portalentidades",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.capitalize(),
            "DB_CLUSTER_ARN": self.aurora_construct.cluster.cluster_arn,
            "DB_SECRET_ARN":  self.aurora_construct.secret.secret_arn,
            "DB_NAME": self.aurora_construct.default_database_name,
            "REGION": Aws.REGION,
            "S3_BUCKET_NAME": self.s3_construct.s3_bucket_users_spreadsheet.bucket_name,
            "GRAPH_MICROSOFT_ENDPOINT": os.environ.get("GRAPH_MICROSOFT_ENDPOINT"),
            "CREATE_USER_ENDPOINT": self.apigw_construct.create_user_endpoint,
            "WARNING_TABLE_NAME": self.dynamo_construct.warning_table.table_name
        }

        self.sm_construct = SmConstruct(
            self, 
            construct_id="SecretsManager",
            stack_name=stack_name,
            stage=stage,
            environment_variables=ENVIRONMENT_VARIABLES
        )

        ENVIRONMENT_VARIABLES["EVENT_SECRET_ARN"] = self.sm_construct.event_secret.secret_arn

        self.lambda_construct = LambdaConstruct(
            self, 
            construct_id="Lambda",
            stack_name=stack_name,
            stage=stage,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES,
            sm_construct=self.sm_construct
        )

        for fn in self.lambda_construct.functions_that_need_aurora_access:
            self.aurora_construct.cluster.grant_data_api_access(fn)
            self.aurora_construct.secret.grant_read(fn)
            
        for fn in self.lambda_construct.functions_that_need_s3_permissions:
            self.s3_construct.s3_bucket_users_spreadsheet.grant_read_write(fn)
            
        for fn in self.lambda_construct.functions_that_need_dynamo_permissions:
            self.dynamo_construct.warning_table.grant_read_write_data(fn)
            
            # needed for gsi access
            # methods that query to gsi will need this additional policy
            # if any other use than query to gsi is needed, this must be adjusted
            fn.add_to_role_policy(iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["dynamodb:Query"],
                resources=[
                    f"{self.dynamo_construct.warning_table.table_arn}/index/*"
                ]
            ))

        