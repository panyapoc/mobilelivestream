#!/bin/bash
sam deploy \
    --stack-name mobilelive \
    --profile mobilelive \
    --region ap-southeast-1 \
    --capabilities CAPABILITY_NAMED_IAM