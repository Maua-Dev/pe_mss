from aws_cdk import (
    aws_secretsmanager as secretsmanager,
)
import json
from constructs import Construct

class SmConstruct(Construct):
    event_secret: secretsmanager.ISecret

    def __init__(
        self,
        scope: Construct,
        environment_variables: dict
    ):
        stage= environment_variables.get("STAGE", "errorStage")
        stack_name= environment_variables.get("STACK_NAME", "errorStackName")

        super().__init__(scope, f"{stack_name}_SmConstruct_{stage}")

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