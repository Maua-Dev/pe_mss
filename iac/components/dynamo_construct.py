from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)
from constructs import Construct


RETAINED_STAGES = {"prod", "homolog"}


class DynamoConstruct(Construct):

    warning_table: dynamodb.Table
    WARNING_TABLE_NAME: str = "PortalEntidadesWarningTable"

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kwargs
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        stage = stage.lower()

        removal_policy = RemovalPolicy.RETAIN if stage in RETAINED_STAGES else RemovalPolicy.DESTROY

        self.warning_table = dynamodb.Table(
            self,
            id="WarningTable",
            partition_key=dynamodb.Attribute(
                name="warning_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            table_name=f"{self.WARNING_TABLE_NAME}-{stage}",
            point_in_time_recovery_specification=dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled=(stage == "prod")
            ),
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
