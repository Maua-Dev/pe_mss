import boto3
from src.shared.environments import Environments
from src.shared.infra.repositories.warning_repository_dynamo import WarningRepositoryDynamo
from src.shared.infra.repositories.warning_repository_mock import WarningRepositoryMock


def setup_warning_table():
    envs = Environments.get_envs()

    table_name = "warnings"
    endpoint = f"{envs.dynamo_endpoint_url}:{envs.dynamo_endpoint_port}"
    
    print(f"Setting up DynamoDB table '{table_name}' at endpoint '{endpoint}'")
    
    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint)
    print("DynamoDB client created")
    
    tables = dynamo_client.list_tables()['TableNames']
    
    if table_name not in tables:
        print(f"Creating table '{table_name}'...")
        dynamo_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'warning_id',
                    'KeyType': 'HASH'
                }
                # {
                #     'AttributeName': 'target_org',
                #     'KeyType': 'RANGE'
                # }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'warning_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'target_org',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'target_role',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'OrganizationIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'target_org',
                            'KeyType': 'HASH'
                        }
                        # {
                        #     'AttributeName': 'warning_id',
                        #     'KeyType': 'RANGE'
                        # }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                },
                {
                    'IndexName': 'RoleIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'target_role',
                            'KeyType': 'HASH'
                        }
                        # {
                        #     'AttributeName': 'warning_id',
                        #     'KeyType': 'RANGE'
                        # }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ]
        )
        
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=table_name)
        
        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists.")
        
        
def load_warning_mock_to_dynamo():
    setup_warning_table()
    mock_repo = WarningRepositoryMock()
    dynamo_repo = WarningRepositoryDynamo()
    
    counter = 0
    
    warnings = mock_repo.get_all_warnings()
    for warning in warnings:
        dynamo_repo.create_warning(warning)
        counter += 1

    print(f"Loaded {counter} warnings into DynamoDB.")

if __name__ == "__main__":
    load_warning_mock_to_dynamo()