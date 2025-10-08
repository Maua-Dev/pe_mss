import os
from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration,
    aws_apigateway as apigw
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class LambdaConstruct(Construct):
   
    def create_lambda_api_gateway_integration(
        self, 
        module_name: str, 
        method: str, 
        mss_student_api_resource: Resource,
        environment_variables: dict = {"STAGE": "TEST"}, 
        authorizer = None
    ):
        
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_student_api_resource.add_resource(
            module_name.replace("_", "-")).add_method(
                method,
                integration=LambdaIntegration(function)
            )

        return function

    def __init__(
        self, 
        scope: Construct, 
        api_gateway_resource: Resource, 
        environment_variables: dict
    ) -> None:
        
        #qdo for fazer o ultimo item voce vai precisar instanciar o authorizer e passar na criacao da lambda
        #pega um exemplo do reservation_api, la tem um authorizer nesse mesmo arquivo
        
        super().__init__(scope, "PortalEntidades_Lambdas")
        
        authorizer_lambda = lambda_.Function(
            self, "AuthorizerPEMssLambda",
            code=lambda_.Code.from_asset("../src/shared/authorizer"),
            handler="graph_authorizer.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self, "TokenAuthorizerPEMssApi",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            authorizer_name="AuthorizerPEMssLambda",
            results_cache_ttl=Duration.seconds(0)
        )

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            "PortalEntidades_Layer",
            # WARNING: O diretório "build" deve ser o mesmo usado em adjust_layer_direcory.py
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11]
        )
        
        self.upload_users_function = self.create_lambda_api_gateway_integration(
            module_name="upload_users",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )
        
        self.create_user_function = self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )
        
        allowed_arns = [self.create_user_function.function_arn]
        authorizer_lambda.add_environment(
            "ALLOWED_LAMBDA_ARNS", ",".join(allowed_arns)
        )

        self.update_user_function = self.create_lambda_api_gateway_integration(
            module_name="update_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.functions_that_need_db_access = [
            self.update_user_function
        ]
        
        self.functions_that_need_s3_permissions = [
            self.upload_users_function
        ]
