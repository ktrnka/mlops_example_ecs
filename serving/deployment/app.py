#!/usr/bin/env python3

from aws_cdk import core as cdk
from stacks.ecs_service import TextClassifierService


app = cdk.App()
TextClassifierService(app, "ExampleEcsTextClassifierStack")
app.synth()
