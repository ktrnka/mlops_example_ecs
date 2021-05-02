from aws_cdk import (core as cdk,
                     aws_ecr_assets as ecr_assets,
                     aws_ecs_patterns as ecs_patterns,
                     aws_ecs as ecs,
                     aws_ec2 as ec2,
                     aws_elasticloadbalancingv2 as elb)

class TextClassifierService(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str):
        super().__init__(scope, id)

        docker_image = ecr_assets.DockerImageAsset(
            self,
            "EcsTextClassifierServiceImage",
            directory="../app"
        )

        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "TextClassifierService",
            # note some pairs of memory and cpu settings are invalid
            memory_limit_mib=512,
            cpu=256,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(docker_image),
                container_port=8000

                # TODO: try environment={git_sha: code_version} for passing info on the build to the execution
            ),
            public_load_balancer=True,

            # new feature that might catch and undo stalled deployments
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True)
        )

        service.target_group.configure_health_check(path="/health")


