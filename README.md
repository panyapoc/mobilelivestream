# Mobile Live Streaming AWS

Mobile Live Streaming Solution on AWS

## Deploy

Howto acc

``` bash
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
```

Mobilelive acc

``` bash
#!/bin/bash
sam package \
    --s3-bucket <> \
    --profile mobilelive

sam deploy \
    --stack-name mobilelive \
    --profile mobilelive \
    --region ap-southeast-1 \
    --s3-bucket <> \
    --capabilities CAPABILITY_NAMED_IAM
```

## DynamoDB Table

### DDB Channel Table

- ChannelId
- Streamer : [Future USE] who currenty Streaming
- Status : IDLE | IN_USE | IN_PROGESS
- RTMPEndpoint : RMTP input Endpoint for mobile to stream to this channel
- MediaPackageHLSEndpoint : HLS Endpoint to view livestream

logging of livestream is p much VOD table

### DDB VoD Table

- VoDID
- ChannelId : Create From which chaneel
- StartTime : Start TS
- EndTime : END TS
- VoDEndPoint : HLS Endpoint to view VoD
- Streamer : [Future USE] who streamed this VoD