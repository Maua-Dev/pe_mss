from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

from ..contructs.lambda_construct import LambdaConstruct
from ..contructs.dynamo_construct import DynamoConstruct
from ..contructs.bucket_construct import BucketContruct


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.rest_api = RestApi(self, "PortalEntidades_RestApi",
                                    rest_api_name="PortalEntidades_RestApi",
                                    description="This is the Portal das Entidades RestApi",
                                    default_cors_preflight_options=
                                    {
                                        "allow_origins": Cors.ALL_ORIGINS,
                                        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                        "allow_headers": ["*"]
                                    },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("pe-mss", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )

        self.dynamo_table = DynamoConstruct(self, "DynamoStack")
        self.s3_bucket = BucketContruct(self)

        ENVIRONMENT_VARIABLES = {
            "STAGE": "DEV",
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.region,
            "S3_BUCKET_NAME": self.s3_bucket.s3_bucket_member.bucket_name
        }

        self.lambda_stack = LambdaConstruct(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)
            
        for function in self.lambda_stack.functions_that_need_s3_permissions:
            self.dynamo_table.table.grant_read_write_data(function)

        