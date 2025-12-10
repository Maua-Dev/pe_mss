import boto3
from src.shared.clients.sm_client import SmClient
from src.shared.environments import Environments
import uuid
from datetime import datetime, timezone
from botocore.exceptions import ClientError
import json

class EventBridgeClient:
    
    def __init__(self):
        self.__envs = Environments.get_envs()
        stage = self.__envs.stage.value
        
        self.delete_warning_lambda_arn = self.__envs.delete_warning_lambda_arn
        
        print("Initializing EventBridge client...")
        
        if stage == "TEST":
            self.eventbridge = boto3.client(
                "events",
                aws_access_key_id=self.__envs.client_id,
                aws_secret_access_key=self.__envs.client_secret,
                endpoint_url=self.__envs.endpoint_url,
                region_name=self.__envs.region,
            )
        else:
            self.eventbridge = boto3.client("events")
    
    def update_trigger_expiration(self, warning_id: str, new_expire: int) -> str:
        """
        Atualiza o tempo de expiração (ScheduleExpression) de uma regra existente no EventBridge.
        """
        # 1. Validar o novo timestamp
        try:
            dt = datetime.fromtimestamp(new_expire / 1000, tz=timezone.utc)
            if dt <= datetime.now(timezone.utc):
                raise ValueError("Timestamp 'new_expire' must be in the future.")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid 'new_expire' timestamp provided: {e}")

        rule_name = f"one-time-trigger-for-alert-{warning_id}"
        cron_expr = f"cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})"
        
        try:
            # 2. Verificar se a regra existe antes de tentar atualizar
            # Isso garante que estamos realmente atualizando, e não criando uma nova regra por acidente.
            print(f"Checking for existence of rule: {rule_name}")
            self.eventbridge.describe_rule(Name=rule_name)
            print(f"Rule found. Attempting to update schedule for: {rule_name}")
            
            # 3. Chamar put_rule para atualizar a regra com a nova expressão cron
            # O EventBridge sobrescreve a configuração da regra existente com o mesmo nome.
            self.eventbridge.put_rule(
                Name=rule_name,
                ScheduleExpression=cron_expr,
                State="ENABLED",
                Description="Rule for deleting a created alert after certain time in the reservation mss alert. This rule triggers a delete alert lambda function"
            )
            
            print(f"Successfully updated schedule for rule: {rule_name}")
            return rule_name

        except ClientError as e:
            # Trata o caso específico em que a regra não foi encontrada
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"ERROR: Cannot update rule '{rule_name}' because it does not exist.")
                # Você pode optar por criar a regra aqui ou simplesmente lançar o erro
                raise e
            else:
                # Trata outros erros possíveis (ex: permissões)
                print(f"ERROR: Failed to update EventBridge rule '{rule_name}'. Reason: {e.response['Error']['Message']}")
                raise e
            
    def delete_trigger(self, rule_name: str) -> str:
        """
        Deleta uma regra do EventBridge e seus alvos associados com base no nome da regra.
        """
        try:
            
            print(f"Attempting to delete rule: {rule_name}")
            
            self.eventbridge.remove_targets(
                Rule = rule_name,
                Ids=["DeleteAlertLambdaTarget"]
            )
            
            print(f"Successfully removed targets from rule: {rule_name}")
            
            self.eventbridge.delete_rule(Name=rule_name)
            
            print(f"Successfully deleted rule: {rule_name}")
            
            return rule_name
            
        except ClientError as e:

            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Rule '{rule_name}' not found. It may have been already deleted.")
            else:
                print(f"ERROR: Failed to delete rule '{rule_name}'. Reason: {e.response['Error']['Message']}")
                raise e
            
    def create_trigger_for_deletion(self, warning_id: str, expire: int) -> str:
        
        # 1. Validate the timestamp first to fail fast
        try:
            dt = datetime.fromtimestamp(expire / 1000, tz=timezone.utc) # turn the time stamp to miliseconds
            if dt <= datetime.now(timezone.utc):
                raise ValueError("Timestamp 'expire' must be in the future.")
            
        except (ValueError, TypeError) as e:
            # Catches invalid timestamps or non-numeric input
            raise ValueError(f"Invalid 'expire' timestamp provided: {e}")

        rule_name = f"one-time-trigger-for-alert-{warning_id}"
        cron_expr = f"cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})"
        
        # 2. Try to create the EventBridge rule
        
        try:
            print(f"Attempting to create rule: {rule_name}")
            self.eventbridge.put_rule(
                Name=rule_name,
                ScheduleExpression=cron_expr,
                State="ENABLED",
                Description="Rule for deleting a created alert after certain time in the reservation mss alert. This rule triggers a delete alert lambda function"
            )
            print(f"Successfully created rule: {rule_name}")
        
        except ClientError as e:
            # Handle exceptions from the put_rule API call (e.g., permissions, invalid expression)
            print(f"ERROR: Failed to create EventBridge rule '{rule_name}'. Reason: {e.response['Error']['Message']}")
            raise Exception(f"Could not create EventBridge rule: {e}")
        
        # 3. Try to add the target to the rule
        try:
            print(f"Attempting to set target for rule: {rule_name}")
            
            body_content = {
                "warning_id": warning_id,
                "rule_name": rule_name,
                "signature": SmClient().sign(rule_name=rule_name, warning_id=warning_id)
            }
            
            lambda_payload = {
                "body": json.dumps(body_content)
            }
            
            input_payload = json.dumps(lambda_payload)
            
            self.eventbridge.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        "Id": "DeleteAlertLambdaTarget",
                        "Arn": self.delete_warning_lambda_arn,
                        "Input": input_payload
                    }
                ]
            )
            print("Successfully set target for rule.")
            
        except ClientError as e:
            print(f"ERROR: Failed to set target for rule '{rule_name}'. Attempting cleanup.")
            
            # CLEANUP: If setting the target fails, try to delete the orphaned rule
            try:
                self.eventbridge.delete_rule(Name=rule_name)
                print(f"Cleanup successful: Deleted orphaned rule '{rule_name}'.")
            except ClientError as cleanup_error:
                # This is a critical failure, as the rule is now orphaned without a target
                print(f"CRITICAL ERROR: Failed to delete orphaned rule '{rule_name}'. Manual cleanup required. Error: {cleanup_error}")
            
            # Propagate the original error after attempting cleanup
            raise Exception(f"Could not set target for EventBridge rule: {e}")
        
        return rule_name