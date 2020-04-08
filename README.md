# Mobile Live Streaming AWS

Mobile Live Streaming Solution on AWS

Deploy

``` bash
sam deploy --stack-name mobilelive --profile mobilelive
```

## DynamoDB Table

### DDB Channel Table

- ChannelID
- Streamer : [Future USE] who currenty Streaming
- Status : IDLE | IN_USE | IN_PROGESS
- RTMPEndpoint : RMTP input Endpoint for mobile to stream to this channel
- MediaPackageHLSEndpoint : HLS Endpoint to view livestream

### DDB VoD Table

- VODID
- ChannelID : Create From which chaneel
- StartTime : Start TS
- EndTime : END TS
- VoDEndPoint : HLS Endpoint to view VoD
- Streamer : [Future USE] who streamed this VoD