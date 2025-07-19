from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct

class CloudfrontDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3バケットを作成（静的ウェブサイトホスティング用）
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            # バケット名は自動生成される（重複を防ぐため）
            removal_policy=RemovalPolicy.DESTROY,  # 開発環境用の設定
            auto_delete_objects=True,  # スタック削除時にオブジェクトも削除
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # セキュリティ強化
        )

        # CloudFrontディストリビューションを作成
        distribution = cloudfront.Distribution(
            self, "WebsiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
            ),
            default_root_object="index.html",
            comment="CloudFront demo distribution created with CDK",
        )

        # ウェブサイトファイルをS3にデプロイ
        s3deploy.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3deploy.Source.asset("../website")],  # websiteディレクトリを指定
            destination_bucket=website_bucket,
            distribution=distribution,  # CloudFrontキャッシュを無効化
            distribution_paths=["/*"],
        )

        # CloudFrontのURLを出力
        CfnOutput(
            self, "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront distribution URL",
        )
