event = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/my/path",
    "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
    "cookies": [
        "cookie1",
        "cookie2"
    ],
    "headers": {
        "header1": "value1",
        "header2": "value1,value2"
    },
    "queryStringParameters": {
        "user_id": "um grande id",
        "inteiro": "5"
    },
    # O QUERY STRING SEMPRE SERÁ USADO NAS ROTAS GET
    # POIS AS ROTAS GET NAO PERMITEM PASSAGEM DE INFORMAÇÕES
    # PELO BODY!! 
    # FIQUEM ATENTOS TB QUE NO QUERRY STRINGS TUDO É TRANSOFRMADO PARA STRINGS, OU SEJA, 
    # SEMPRE EM UMA ROTA GET QUE RECEBEMOS INFORMACÕES NUMERICAS OU BOOLEANAS PRECISAMOS CONVERTELAS DE STRINGS
    # PARA SEUS RESPECTIOVOS TIPOS
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "<urlid>",
        "authentication": None,
        "authorizer": {
            
            # O USUARIO SERA RECEBIDO EXATAMENTE COMO ESTA DESCRITO A BAIXO, COM OS MESMO PARAMTROS
            # TEMOS QUE EXTRAIR ESSES PARAMETROS PARA CRIAR O USUARIO / SABER QUEM É O USUARIO FAZENDO
            # A REQUISIÇÃO. PARA CRIAR O RA DO ALUNO / USUARIO, TEMOS QUE PEGAR A PRIMEIRA PARTE DO EMAIL ANTES DO
            # @MAUA.BR. O ID NAO PRECISARA SER CRIADO, POIS JA ESTARA PRESENTE AQUI NESSE USUARIO, OU SEJA, APENAS
            # PRECISARA SER PEGO PELA ROTA E PASSADO PARA A NOVA ENTIDADE A SER CRIADA
            
            "user": {
                "id": "Lebron James 1337",
                "displayName": "Lebron James",
                "email": "Lebron.James@maua.br"
            }
        },
        "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
        "domainPrefix": "<url-id>",
        "external_interfaces": {
            "method": "POST",
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "sourceIp": "123.123.123.123",
            "userAgent": "agent"
        },
        "requestId": "id",
        "routeKey": "$default",
        "stage": "$default",
        "time": "12/Mar/2020:19:03:58 +0000",
        "timeEpoch": 1583348638390
    },
    # O BODY SERA USADO EM TODOS AS ROTAS POSTS E DIFERENTEMENTE DO QUERRY ELE PERMITE TIPOS DIFERENTES DE STRINGS
    # O BODY TAMBEM É ACESSIVEL PARA ROTAS DO TIPO PUT
    "body": {"edl_value": 5, "nome": "ABCDE", "is_rule": False},
    "pathParameters": None,
    "isBase64Encoded": None,
    "stageVariables": None
}