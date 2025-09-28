import os
#test uploading
import aws_cdk as cdk
from aws_cdk import (
    aws_s3,
    aws_stepfunctions,
    aws_iam,
    aws_cloudfront, aws_cloudfront_origins, RemovalPolicy
)

from constructs import Construct


class BucketContruct(Construct):
    s3_bucket_user: aws_s3.Bucket
    selfie_validation_step_function: aws_stepfunctions.StateMachine
    cloudfront_distribution_member: aws_cloudfront.Distribution
    
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "PortalEntidades_Bucket")
        
        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY
        
        self.s3_bucket_user = aws_s3.Bucket(
            self, 
            "PortalEntidades_User_Bucket",
            versioned=True,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            event_bridge_enabled=True,
            cors=[aws_s3.CorsRule(
                allowed_methods=[
                    aws_s3.HttpMethods.GET, 
                    aws_s3.HttpMethods.PUT, 
                    aws_s3.HttpMethods.POST
                ],
                allowed_origins=["*"],
                allowed_headers=["*"],
                max_age=3000
            )],
            removal_policy=REMOVAL_POLICY
        )

        oac = aws_cloudfront.CfnOriginAccessControl(
            self, 
            "PortalEntidades_User_Bucket_OAC",
            origin_access_control_config=aws_cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name="PortalEntidadesUserBucketOAC",
                origin_access_control_origin_type="s3",
                signing_behavior="always",
                signing_protocol="sigv4"
            )
        )

        self.cloudfront_distribution_member = aws_cloudfront.Distribution(
            self,
            "PortalEntidades_User_Bucket_CloudFront_Distribution",
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3BucketOrigin(self.s3_bucket_user),
                origin_request_policy=aws_cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                response_headers_policy=aws_cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS,
                cache_policy=aws_cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=aws_cloudfront.AllowedMethods.ALLOW_ALL
            )
        )

        cfn_distribution = self.cloudfront_distribution_member.node.default_child
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.OriginAccessControlId", 
            oac.attr_id
        )
        
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.S3OriginConfig.OriginAccessIdentity",
            ""
        )

        self.s3_bucket_user.add_to_resource_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ServicePrincipal("cloudfront.amazonaws.com")],
                actions=["s3:GetObject"],
                resources=[f"{self.s3_bucket_user.bucket_arn}/*"],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{cdk.Stack.of(self).account}:distribution/{self.cloudfront_distribution_member.distribution_id}"
                    }
                }
            )
        )