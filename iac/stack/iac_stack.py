from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam
)


from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

# Aqui não precisamos importar subindo um diretório pois a execução acontece diretamente do diretório iac
from components.aurora_construct import AuroraConstruct
from components.lambda_construct import LambdaConstruct
from components.bucket_construct import BucketContruct
from components.dynamo_construct import DynamoConstruct
from components.sm_construct import SmConstruct
from components.apigw_component import ApigwComponent
import os

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = kwargs['tags']['stage']
        
        self.apigw_component = ApigwComponent(self, "Apigw")
        self.dynamo_construct = DynamoConstruct(self, "PEDynamo")
        self.aurora = AuroraConstruct(self, "Aurora")
        self.s3_bucket = BucketContruct(self)

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DB_CLUSTER_ARN": self.aurora.cluster.cluster_arn,
            "DB_SECRET_ARN":  self.aurora.secret.secret_arn,
            "DB_NAME": self.aurora.default_database_name,
            "REGION": self.region,
            "S3_BUCKET_NAME": self.s3_bucket.s3_bucket_user.bucket_name,
            "GRAPH_MICROSOFT_ENDPOINT": os.environ.get("GRAPH_MICROSOFT_ENDPOINT"),
            "WARNING_TABLE_NAME": self.dynamo_construct.warning_table.table_name
        }

        self.sm_construct= SmConstruct(self, environment_variables=ENVIRONMENT_VARIABLES)

        ENVIRONMENT_VARIABLES["EVENT_SECRET_ARN"]= self.sm_construct.event_secret.secret_arn

        self.lambda_construct = LambdaConstruct(
            self, 
            api_gateway_resource=self.apigw_component.api_gateway_resource,
            rest_api=self.apigw_component.rest_api,
            environment_variables=ENVIRONMENT_VARIABLES,
            sm_construct=self.sm_construct
        )

        for fn in self.lambda_construct.functions_that_need_db_access:
            self.aurora.cluster.grant_data_api_access(fn)
            self.aurora.secret.grant_read(fn)
            
        for fn in self.lambda_construct.functions_that_need_s3_permissions:
            self.s3_bucket.s3_bucket_user.grant_read_write(fn)
            
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

        