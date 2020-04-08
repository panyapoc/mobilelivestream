# CloudWatch Channel State Change Event idle -> Running
# 1. Update Channel State on DDB
# 2. Update VoD table
# 3. Notify Mobile Channel Ready

# CloudWatch Channel State Change Event Running -> Idle
# 1. Update Channel State on DDB
# 2. Start moving archive file to new location
# 3. Create .m3u8 file from list of .ts file
# 4. Add new .m3u8 to DDB for future playing
# 5. Update VoD table

import boto3
import json
import os
import uuid
from datetime import datetime

# BOTO3
medialive = boto3.client('medialive')
dynamodb = boto3.resource("dynamodb")
sns = boto3.client('sns')

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])
ddb_vod = dynamodb.Table(os.environ['ddb_vod'])

def lambda_handler(event, context):
    # CloudWatch Channel State Change Event idle -> Running
    # 1. Update Channel State on DDB
    # 2. Update VoD table
    # 3. Notify Mobile Channel Ready
    if event['detail']['state'] == 'RUNNING' :
        ChannelID = getChannelID(event['detail']['channel_arn'])
        print(f'updating channel {ChannelID} State to RUNNING')
        ddb_channel.update_item(
            Key={
                'ChannelID': ChannelID
            },
            UpdateExpression='set #keyState = :State',
            ExpressionAttributeNames={
                '#keyState' : 'State',
            },
            ExpressionAttributeValues={
                ':State': 'RUNNING'
            }
        )

        timestamp = datetime.timestamp(datetime.now())
        print("timestamp =", timestamp)

        VoD = {
            'VoDID' : str(uuid.uuid4()),
            'ChannelId' : ChannelID,
            'StartTime' : str(timestamp),
            'EndTime' : None,
            'VoDEndpoint' : None,
            'Streamer' : None
        }
        ddb_vod.put_item(Item=VoD)

        Channel = ddb_channel.get_item(
            Key={ 'ChannelID': ChannelID }
        )
        ChannelRTMPEndpoint = Channel['Item']['RTMPEndpoint']
        Message = {
            'Message' : f'Channel {ChannelID} is ready',
            'RTMPEndpoint' : ChannelRTMPEndpoint
        }
        print(Message)
        sns_publish = sns.publish(
            TopicArn=os.environ['snstopic'],
            Message=json.dumps(Message),
            MessageStructure='string',
        )
        return 'ok'


    # CloudWatch Channel State Change Event Running -> Idle
    # 1. Start moving archive file to new location
    # 2. Create .m3u8 file from list of .ts file
    # 3. Add new .m3u8 to DDB for future playing
    # 4. Update VoD table
    # 5. Update Channel State on DDB ✅
    elif event['detail']['state'] == 'STOPPED' :
        ChannelID = getChannelID(event['detail']['channel_arn'])
        print(f'updating channel {ChannelID} State to STOPPED')
        ddb_channel.update_item(
            Key={
                'ChannelID': ChannelID
            },
            UpdateExpression='set #keyState = :State',
            ExpressionAttributeNames={
                '#keyState' : 'State',
            },
            ExpressionAttributeValues={
                ':State': 'IDLE'
            }
        )

        return 'ok'


    return 'ok'

def getChannelID (ChannelARN) :
    return ChannelARN.rsplit(':',1)[1]