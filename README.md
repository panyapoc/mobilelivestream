# Mobile Live Streaming AWS

Mobile Live Streaming Solution on AWS

## Encoding Consideration

- [Twitch Encoding recommendation](https://stream.twitch.tv/encoding/)
- [YT Encoding recommendation](https://support.google.com/youtube/answer/2853702?hl=en)
-
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
- State : IDLE | IN_USE | IN_PROGESS
- RTMPEndpoint : RMTP input Endpoint for mobile to stream to this channel
- MediaPackageHLSEndpoint : HLS Endpoint to view livestream
- VoDS3key : S3 key folder

logging of livestream is p much VOD table

### DDB VoD Table

- VoDID
- ChannelId : Create From which chaneel
- StartTime : Start TS
- EndTime : END TS
- VoDEndpoint : HLS Endpoint to view VoD
- Streamer : [Future USE] who streamed this VoD

Timestamp Usage

``` Python
from datetime import datetime

# current date and time
now = datetime.now()

timestamp = datetime.timestamp(now)
print("timestamp =", timestamp)


timestamp = 1545730073
dt_object = datetime.fromtimestamp(timestamp)

print("dt_object =", dt_object)
print("type(dt_object) =", type(dt_object))
```