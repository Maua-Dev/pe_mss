import hmac
import hashlib
import base64
import boto3
import json
import os


class SmClient:
    def __init__(self):
        self._secrets = boto3.client("secretsmanager")
        self._cached_secret = None

    def get_secret(self):
        if self._cached_secret:
            return self._cached_secret

        arn = os.environ["EVENT_SECRET_ARN"]
        resp = self._secrets.get_secret_value(SecretId=arn)
        secret = json.loads(resp["SecretString"])["EVENT_SECRET"]

        self._cached_secret = secret
        return secret

    def sign(self, rule_name: str, warning_id: str) -> str:
        secret = self.get_secret()
        raw = f"{rule_name}:{warning_id}"
        digest = hmac.new(secret.encode(), raw.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def verify(self, rule_name: str, warning_id: str, signature: str) -> bool:
        try:
            expected = self.sign(rule_name, warning_id)
            return hmac.compare_digest(expected, signature)
        except Exception as e:
            print(f"Erro na verificação: {e}")
            return False