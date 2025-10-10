import os
from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class DynamoDBWarningConstruct(Construct):
    """
    CDK Construct to create the DynamoDB table for Warnings.
    Includes separate GSIs for querying by Organization and Role.
    """
    
    table: dynamodb.Table

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = os.environ.get("STAGE", "DEV").upper()

        is_prod = (stage == "PROD")
        removal_policy = RemovalPolicy.RETAIN if is_prod else RemovalPolicy.DESTROY
        
        table_name = f"PortalEntidadesWarningTable-{stage}"
        
        self.table = dynamodb.Table(
            self, "PortalEntidadesWarningTable",
            table_name=table_name,
            
            partition_key=dynamodb.Attribute(
                name="warning_id",
                type=dynamodb.AttributeType.STRING
            ),
            global_secondary_indexes=[
                dynamodb.GlobalSecondaryIndexProps(
                    index_name="OrganizationIndex",
                    partition_key=dynamodb.Attribute(
                        name="target_org",
                        type=dynamodb.AttributeType.STRING
                    ),
                    projection_type=dynamodb.ProjectionType.ALL
                ),
                dynamodb.GlobalSecondaryIndexProps(
                    index_name="RoleIndex",
                    partition_key=dynamodb.Attribute(
                        name="target_role",
                        type=dynamodb.AttributeType.STRING
                    ),
                    projection_type=dynamodb.ProjectionType.ALL
                )
            ],
            
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            point_in_time_recovery=is_prod
        )