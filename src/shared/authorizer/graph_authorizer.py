import os
import json
import logging
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED = os.getenv("ALLOWED_LAMBDA_ARNS", "").split(",")

def lambda_handler(event, context):
    """
    Autoriza o usuário validando seu token diretamente contra a API do Microsoft Graph.
    Permite o acesso se a API retornar sucesso (200 OK), caso contrário, nega.
    """
    
    arn_caller = event.get("requestContext", {}).get("identity", {}).get("callerArn")
    
    if arn_caller in ALLOWED:
        # permitir sem token caso o arn corresponda com allowed
        return {
            "principalId": "lambda-access",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["methodArn"]
                    }
                ]
            }
        }
    
    logger.info("Iniciando processo de autorização via Microsoft Graph.")

    # É essencial ter o method_arn para gerar a política, mesmo em caso de falha.
    method_arn = event.get("methodArn")
    if not method_arn:
        logger.error("'methodArn' não foi encontrado no evento do authorizer.")
        # Sem o ARN, o API Gateway retornará 500. Não há como gerar uma política.
        raise Exception("Configuração do Authorizer inválida: methodArn ausente.")

    try:
        # 1. Obter o endpoint da Microsoft a partir das variáveis de ambiente
        graph_endpoint = os.environ["GRAPH_MICROSOFT_ENDPOINT"]

        # 2. Extrair o token do cabeçalho da requisição
        token = _get_token_from_event(event)

        # 3. Fazer a chamada para a API do Microsoft Graph para validar o token
        # Esta função irá retornar os dados do usuário em caso de sucesso
        # ou lançar uma exceção em caso de falha.
        user_data = _fetch_user_from_graph(token, graph_endpoint)
        
        # O ID do usuário retornado pelo Graph API será o 'principalId' na política
        principal_id = user_data.get("id", "user")
        
        logger.info(f"Token válido. Autorização concedida para o principalId: {principal_id}")

        # 4. Se a chamada foi bem-sucedida, gerar uma política de permissão (Allow)
        # O contexto pode ser usado para passar dados do usuário para a função de backend
        context_data = {"user": json.dumps(user_data)}
        policy = generate_policy(principal_id, "Allow", method_arn, context_data)

        print(policy)
        
        return policy

    except (KeyError, ValueError) as e:
        # Captura erros de configuração (variável de ambiente faltando) ou de formato do token
        logger.error(f"Erro de configuração ou requisição inválida: {e}")
        return generate_policy("user", "Deny", method_arn)
    except Exception as e:
        # Captura qualquer outra exceção, incluindo falhas na chamada com urllib3
        logger.error(f"Falha na autorização: {e}")
        return generate_policy("user", "Deny", method_arn)


def _get_token_from_event(event):
    """Extrai e valida o formato do token 'Bearer' do evento."""
    auth_header = event.get("authorizationToken")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("Token de autorização 'Bearer' ausente ou mal formatado.")
    return auth_header.replace("Bearer ", "")


def _fetch_user_from_graph(token, endpoint):
    """
    Usa urllib3 para buscar informações do usuário na API do Microsoft Graph.
    Retorna os dados do usuário em caso de sucesso ou lança uma exceção em caso de falha.
    """
    http = urllib3.PoolManager()
    headers = {"Authorization": f"Bearer {token}"}
    
    logger.info(f"Fazendo requisição GET para: {endpoint}")
    
    response = http.request("GET", endpoint, headers=headers)

    if response.status != 200:
        # Logar o erro para depuração, sem expor dados sensíveis se possível
        error_body = response.data.decode('utf-8', errors='ignore')
        logger.error(f"Microsoft Graph API retornou status {response.status}. Corpo: {error_body}")
        raise Exception("Falha ao validar o token com a API da Microsoft.")

    # Decodifica a resposta e a converte de JSON para um dicionário Python
    user_data = json.loads(response.data.decode("utf-8"))
    return user_data


def generate_policy(principal_id, effect, method_arn, context=None):
    """Gera o documento de política do IAM para o API Gateway."""
    auth_response = {"principalId": principal_id}

    if effect and method_arn:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn,
                }
            ],
        }
        auth_response["policyDocument"] = policy_document

    if context:
        auth_response["context"] = context

    return auth_response