#!/usr/bin/env python3
import os

import aws_cdk as cdk
from adjust_layer_directory import adjust_layer_directory

from stack.iac_stack import IacStack



print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory()
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")

if 'prod' in stack_name:
    stage = 'PROD'

elif 'homolog' in stack_name:
    stage = 'HOMOLOG'

elif 'dev' in stack_name:
    stage = 'DEV'

else:
    stage = 'TEST'

tags = {
    'project': 'PortalEntidades',
    'stage': stage,
    'stack': 'BACK',
    'owner': 'DevCommunity'
}

IacStack(
    scope=app,
        construct_id="IacStack",
    stack_name=stack_name, 
    env=cdk.Environment(account=aws_account_id, region=aws_region), 
    tags=tags
)


app.synth()
