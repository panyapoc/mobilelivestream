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
s3 = boto3.resource('s3')

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])
ddb_vod = dynamodb.Table(os.environ['ddb_vod'])
archive_s3 = os.environ['archive_s3']
vod_s3key = os.environ['vod_s3key']
CloudFrontVoDURL = os.environ['CloudFrontVoDURL']

def lambda_handler(event, context):
    # CloudWatch Channel State Change Event idle -> Running
    # 1. Update Channel State on DDB
    # 2. Update VoD table
    # 3. Notify Mobile Channel Ready
    if event['detail']['state'] == 'RUNNING' :
        ChannelID = getChannelID(event['detail']['channel_arn'])
        print(f'updating channel {ChannelID} State to RUNNING')

        VoDID = str(uuid.uuid4())

        ddb_channel.update_item(
            Key={
                'ChannelID': ChannelID
            },
            UpdateExpression='set #keyState = :State, VoDID = :VoDID',
            ExpressionAttributeNames={
                '#keyState' : 'State',
            },
            ExpressionAttributeValues={
                ':State': 'RUNNING',
                ':VoDID': VoDID
            }
        )

        timestamp = datetime.timestamp(datetime.now())
        print("start timestamp =", timestamp)

        VoD = {
            'VoDID' : VoDID,
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

        Channel = ddb_channel.get_item(
            Key={ 'ChannelID': ChannelID }
        )

        # 1. Start moving archive file to new location
        origins3key = Channel['Item']['VoDS3key']
        VoDID = Channel['Item']['VoDID']
        for obj in s3.Bucket(archive_s3).objects.filter(Prefix=origins3key):
            # Copy object A as object B
            filename = getFilename(obj.key)
            print(f'src: {obj.key}')
            print(f'destination: {vod_s3key}/{VoDID}/{filename}')
            copy_source = {
                'Bucket': archive_s3,
                'Key': obj.key
            }
            destbucket = s3.Bucket('panyapoc-test-vod')
            obj = destbucket.Object(f'{vod_s3key}/{VoDID}/{filename}')
            obj.copy(copy_source)

        for obj in s3.Bucket(archive_s3).objects.filter(Prefix=origins3key):
            s3.Object(archive_s3, obj.key).delete()
            print(f'deleted {obj.key}')

        # 2. Create .m3u8 file from list of .ts file


        # 3. Add new .m3u8 to DDB for future playing
        # 4. Update VoD table
        timestamp = datetime.timestamp(datetime.now())
        print("end timestamp =", timestamp)
        VoDEndpoint = f'{CloudFrontVoDURL}/{vod_s3key}/{VoDID}/index.m3u8'
        ddb_vod.update_item(
            Key={
                'VoDID': VoDID
            },
            UpdateExpression='set EndTime = :EndTime, VoDEndpoint = :VoDEndpoint',
            ExpressionAttributeValues={
                ':EndTime': str(timestamp),
                ':VoDEndpoint' : VoDEndpoint
            }
        )

        # 5. Update Channel State on DDB ✅
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


def getFilename (s3key) :
    return s3key.rsplit('/',1)[1]