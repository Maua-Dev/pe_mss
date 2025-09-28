from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

from ..contructs.aurora_construct import AuroraConstruct
from ..contructs.lambda_construct import LambdaConstruct
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

        self.aurora = AuroraConstruct(self, "Aurora")
        self.s3_bucket = BucketContruct(self)

        ENVIRONMENT_VARIABLES = {
            "STAGE": "DEV",
            "DB_CLUSTER_ARN": self.aurora.cluster.cluster_arn,
            "DB_SECRET_ARN":  self.aurora.secret.secret_arn,
            "DB_NAME": self.aurora.default_database_name,
            "REGION": self.region,
            "S3_BUCKET_NAME": self.s3_bucket.s3_bucket_member.bucket_name
        }

        self.lambda_stack = LambdaConstruct(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        for fn in self.lambda_stack.functions_that_need_db_access:
            self.aurora.cluster.grant_data_api_access(fn)
            self.aurora.secret.grant_read(fn)
            self.s3_bucket.s3_bucket_member.grant_read_write(fn)

        