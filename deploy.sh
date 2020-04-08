#!/bin/bash
sam package \
    --s3-bucket panyapoc-sgsrc \
    --profile howto

sam deploy \
    --stack-name mobilelive \
    --profile howto \
    --region ap-southeast-1 \
    --s3-bucket panyapoc-sgsrc \
    --capabilities CAPABILITY_NAMED_IAM