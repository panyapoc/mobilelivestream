#!/bin/bash
sam package \
    --s3-bucket panyapoc-sgsrc

sam deploy \
    --stack-name mobilelive \
    --profile howto \
    --region ap-southeast-1 \
    --capabilities CAPABILITY_NAMED_IAM