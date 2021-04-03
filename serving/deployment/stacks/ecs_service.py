from aws_cdk import (core as cdk,
                     aws_ecr_assets as ecr_assets,
                     aws_ecs_patterns as ecs_patterns,
                     aws_ecs as ecs,
                     aws_ec2 as ec2)

class TextClassifierService(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str):
        super().__init__(scope, id)

        docker_image = ecr_assets.DockerImageAsset(
            self,
            "EcsTextClassifierServiceImage",
            directory="../app"
        )

        cluster = ecs.Cluster(
            self,
            "TextClassifierCluster"
        )

        cluster.add_capacity(
            "TextClassifierScalingGroup",
            instance_type=ec2.InstanceType("t3.small"),
            desired_capacity=1,
            max_capacity=4,
            min_capacity=1
        )

        service = ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "TextClassifierService",
            cluster=cluster,
            memory_limit_mib=1024,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(docker_image),
            ),
            min_healthy_percent=50,
            public_load_balancer=True
        )

