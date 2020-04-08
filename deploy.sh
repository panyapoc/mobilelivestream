#!/bin/bash
sam deploy \
    --stack-name mobilelive \
    --profile howto \
    --region ap-southeast-1 \
    --capabilities CAPABILITY_NAMED_IAM