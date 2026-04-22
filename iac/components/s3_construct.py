from aws_cdk import (
    aws_s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    RemovalPolicy,
    Duration,
    Aws
)

from constructs import Construct


RETAINED_STAGES = {"prod", "homolog"}


class S3Construct(Construct):
    s3_bucket_users_spreadsheet: aws_s3.Bucket
    cloudfront_distribution_users_spreadsheet: cloudfront.Distribution
    stack_name: str
    stage: str

    def _build_distribution(
        self,
        distribution_id: str,
        bucket: aws_s3.Bucket,
        default_ttl: Duration,
    ) -> cloudfront.Distribution:
        cache_policy = cloudfront.CachePolicy(
            self,
            f"{distribution_id}CachePolicy",
            cache_policy_name=f"{self.stack_name}-{distribution_id}-Cache-{self.stage}",
            comment=f"Cache policy for {distribution_id}",
            min_ttl=Duration.seconds(1),
            max_ttl=Duration.days(365),
            default_ttl=default_ttl,
            enable_accept_encoding_gzip=True,
            enable_accept_encoding_brotli=True,
        )

        origin_request_policy = cloudfront.OriginRequestPolicy(
            self,
            f"{distribution_id}OriginRequestPolicy",
            origin_request_policy_name=f"{self.stack_name}-{distribution_id}-ORP-{self.stage}",
            comment=f"Origin request policy for {distribution_id}",
            header_behavior=cloudfront.OriginRequestHeaderBehavior.allow_list(
                "Origin",
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method",
            ),
        )

        return cloudfront.Distribution(
            self,
            id=distribution_id,
            comment=f"{self.stack_name} {distribution_id} S3 CDN {self.stage}",
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(bucket),
                compress=True,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cache_policy,
                origin_request_policy=origin_request_policy,
                response_headers_policy=cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS_WITH_PREFLIGHT,
            ),
        )

    def create_bucket_with_distribution(
        self,
        *,
        bucket_id: str,
        bucket_name: str,
        default_ttl: Duration
    ) -> tuple[aws_s3.Bucket, cloudfront.Distribution]:
        bucket = aws_s3.Bucket(
            self,
            id=f"{bucket_id}Bucket",
            bucket_name=bucket_name,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=self.removal_policy,
            auto_delete_objects=self.removal_policy == RemovalPolicy.DESTROY,
        )

        distribution = self._build_distribution(
            distribution_id=f"{bucket_id}Distribution",
            bucket=bucket,
            default_ttl=default_ttl,
        )

        return bucket, distribution

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stack_name: str,
        stage: str,
        **kargs
    ) -> None:

        super().__init__(scope, construct_id, **kargs)

        self.stack_name = stack_name
        self.stage = stage.lower()
        self.removal_policy = (
            RemovalPolicy.RETAIN if self.stage in RETAINED_STAGES else RemovalPolicy.DESTROY
        )

        identifier = f"{Aws.ACCOUNT_ID}-{Aws.REGION}"

        bucket_name = (
            f"{stack_name}-users-spreadsheet-{self.stage}-{identifier}"
            .lower()
            .replace("_", "-")
        )

        self.s3_bucket_users_spreadsheet, self.cloudfront_distribution_users_spreadsheet = (
            self.create_bucket_with_distribution(
                bucket_id="UsersSpreadsheet",
                bucket_name=bucket_name,
                default_ttl=Duration.seconds(30),
            )
        )
