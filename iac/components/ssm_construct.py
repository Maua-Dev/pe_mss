from constructs import Construct
from aws_cdk import Resource, aws_ssm as ssm
from aws_cdk.aws_apigateway import RestApi
from aws_cdk import aws_s3 as s3


class SsmConstruct(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage: str,
        mss_name_identification_for_path: str,
        api: RestApi,
        api_gateway_resource: Resource,
        buckets: dict[str, s3.Bucket] = None,
        extra_params: dict[str, str] = None,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # stage lower é necessário aqui pois no actions do front, stage é recebido como lower
        stage = stage.lower()

        mss_name_identification_for_path = mss_name_identification_for_path.lower().replace("-", "_")

        if api:
            # a '/' final é necessária pois no CD do front contamos como se ela já estivesse lá
            ssm.StringParameter(
                self,
                id="ApiUrl",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/api/url",
                string_value=f"{api.url}{api_gateway_resource.path.lstrip('/')}/"
            )

        for logical_name, bucket in (buckets or {}).items():
            safe_id = logical_name.replace("/", "_").replace("-", "_")
            ssm.StringParameter(
                self,
                id=f"Bucket{safe_id.title().replace('_', '')}",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/buckets/{logical_name}",
                string_value=bucket.bucket_name
            )

        for key, value in (extra_params or {}).items():
            safe_id = key.replace("/", "_").replace("-", "_")
            ssm.StringParameter(
                self,
                id=f"Extra{safe_id.title().replace('_', '')}",
                parameter_name=f"/{mss_name_identification_for_path}/{stage}/{key}",
                string_value=value
            )
