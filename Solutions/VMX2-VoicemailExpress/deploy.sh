#!/bin/bash

AWS_DEFAULT_PROFILE="robinSandbox"
STACK_NAME="voicemail-solution"
AWS_REGION="eu-west-2"
CONNECT_CTR_STREAM_ARN="arn:aws:kinesis:eu-west-2:525716403383:stream/CTR"
CONNECT_INSTANCE_ALIAS="instance-ccp"
CONNECT_INSTANCE_ARN="arn:aws:connect:eu-west-2:525716403383:instance/c9d3df31-a5a0-4e81-b455-384cc6f48161"
ENABLE_VM_TO_CONNECT_TASK="false"
ENABLE_VM_TO_EMAIL="true"
ENABLE_VM_TO_SALESFORCE_CASE="false"
ENABLE_VM_TO_SALESFORCE_CUSTOM_OBJECT="false"
LAMBDA_LOGGING_LEVEL="DEBUG"
VM_TO_EMAIL_DEFAULT_FROM="robin97engineer@gmail.com"
VM_TO_EMAIL_DEFAULT_TO="robin.hedwig@cx.studio"
VM_TEST_AGENT_ID="robin.hedwig@cx.studio"
VM_TEST_QUEUE_ARN="arn:aws:connect:eu-west-2:525716403383:instance/c9d3df31-a5a0-4e81-b455-384cc6f48161/queue/d50ba602-67d1-48aa-a0fe-e4aa461b2823"

# Validate CloudFormation template
sam validate -t ./CloudFormation/vmx.yaml --lint

# Build Template
echo "Build Template"
sam build -t ./CloudFormation/vmx.yaml -b .aws-sam

# Deploy SAM application
sam deploy --profile "$AWS_DEFAULT_PROFILE"\
  --template-file .aws-sam/template.yaml \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --s3-prefix $STACK_NAME \
  --resolve-s3 \
  --region $AWS_REGION \
  --parameter-overrides \
    StackName=$STACK_NAME \
    AWSRegion=$AWS_REGION \
    ConnectCTRStreamARN=$CONNECT_CTR_STREAM_ARN \
    ConnectInstanceAlias=$CONNECT_INSTANCE_ALIAS \
    ConnectInstanceARN=$CONNECT_INSTANCE_ARN \
    EnableVMToConnectTask=$ENABLE_VM_TO_CONNECT_TASK \
    EnableVMToEmail=$ENABLE_VM_TO_EMAIL \
    EnableVMToSalesforceCase=$ENABLE_VM_TO_SALESFORCE_CASE \
    EnableVMToSalesforceCustomObject=$ENABLE_VM_TO_SALESFORCE_CUSTOM_OBJECT \
    LambdaLoggingLevel=$LAMBDA_LOGGING_LEVEL \
    VMToEmailDefaultFrom=$VM_TO_EMAIL_DEFAULT_FROM \
    VMToEmailDefaultTo=$VM_TO_EMAIL_DEFAULT_TO \
    VMTestAgentId=$VM_TEST_AGENT_ID \
    VMTestQueueARN=$VM_TEST_QUEUE_ARN \
    RecordingsExpireInXDays=$RECORDINGS_EXPIRE_IN_X_DAYS \
  --disable-rollback

