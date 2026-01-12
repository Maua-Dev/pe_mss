from aws_cdk import (
    aws_secretsmanager as secretsmanager,
)
import json
from constructs import Construct

class SmStack(Construct):
    event_secret: secretsmanager.ISecret

    def __init__(
        self,
        scope: Construct,
        environment_varibles: dict
    ):
        stage= environment_varibles.get("STAGE", "errorStage")
        stack_name= environment_varibles.get("STACK_NAME", "errorStackName")

        super().__init__(scope, f"{stack_name}_SmStack_{stage}")

        self.event_secret= secretsmanager.Secret(
            self,
            "EventBridgeDeleteSecret",
            description="Secret used to sign EventBridge delete trigger",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"EVENT_SECRET": ""}),
                generate_string_key="EVENT_SECRET",
                password_length=64,
                exclude_punctuation=True
            )
        )