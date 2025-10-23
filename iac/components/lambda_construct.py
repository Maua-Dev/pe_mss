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
                integration=LambdaIntegration(function),
                authorizer=authorizer
            )

        return function

    def __init__(
        self, 
        scope: Construct, 
        api_gateway_resource: Resource, 
        environment_variables: dict
    ) -> None:
        
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
        
        allowed_arns = [self.upload_users_function.function_arn]
        authorizer_lambda.add_environment(
            "ALLOWED_LAMBDA_ARNS", ",".join(allowed_arns)
        )
        
        self.auth_user_function= self.create_lambda_api_gateway_integration(
            module_name="auth_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_all_users_function= self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_user_function = self.create_lambda_api_gateway_integration(
            module_name="get_user",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.create_user_function= self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )
        
        self.delete_user_function= self.create_lambda_api_gateway_integration(
            module_name="delete_user",
            method="DELETE",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.functions_that_need_db_access = [
            self.auth_user_function,
            self.create_user_function,
            self.delete_user_function,
            self.upload_users_function,
            self.get_all_users_function
        ]
        
        self.functions_that_need_s3_permissions = [
            self.upload_users_function
        ]
