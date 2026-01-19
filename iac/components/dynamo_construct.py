from decimal import Decimal
from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct
import os


class DynamoConstruct(Construct):
    
    warning_table: dynamodb.Table
    WARNING_TABLE_NAME: str = "PortalEntidadesWarningTable"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.stack_name = os.environ.get("STACK_NAME")
        stage = ''
        
        if 'prod' in self.github_ref_name.lower():
            stage = 'PROD'            
        elif 'homolog' in self.github_ref_name.lower():
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'
            
        removal_policy = RemovalPolicy.RETAIN if stage=="PROD" else RemovalPolicy.DESTROY

        self.warning_table = dynamodb.Table(
            self, "PortalEntidades_WarningTable",
            partition_key=dynamodb.Attribute(
                name="warning_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="target_org",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
        
            table_name=f"{self.WARNING_TABLE_NAME}-{stage.upper()}",
            point_in_time_recovery=True if stage=="PROD" else False
        )
        
        self.warning_table.add_global_secondary_index(
            index_name="RoleOrgIndex",
            partition_key=dynamodb.Attribute(
                name="target_role",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="target_org",
                type=dynamodb.AttributeType.STRING
            )
        )
        