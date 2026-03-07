from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors
import os

class ApigwComponent(Construct):
    
    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        
        github_ref_name = (os.environ.get("GITHUB_REF_NAME") or "").lower()
        if "prod" in github_ref_name:
            stage = "PROD"
        elif "homolog" in github_ref_name:
            stage = "HOMOLOG"
        else:
            stage = "DEV"

        self.rest_api = RestApi(
            self, 
            id_=f"PortalEntidades_RestApi",
            rest_api_name=f"PortalEntidades_RestApi",
            description=f"This is the Portal das Entidades RestApi",
            default_cors_preflight_options=
            {
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["*"]
            },
            deploy_options={
                "stage_name": stage.lower()
            }
        )

        self.api_gateway_resource = self.rest_api.root.add_resource(
            "pe-mss", 
            default_cors_preflight_options = {
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": Cors.DEFAULT_HEADERS
            }
        )