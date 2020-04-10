# API - ChannelId
# 1. stop Channel
# 2. return ACK

import boto3
import json
import os

# BOTO3
medialive = boto3.client('medialive')
dynamodb = boto3.resource("dynamodb")

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])

def lambda_handler(event, context):
    ChannelId = json.loads(event['body']).get('ChannelId',False) # ChannelId or False
    if ChannelId:
        try:
            medialive_stop_channel = medialive.stop_channel(
                ChannelId=ChannelId
            )
        except:
            response = {
                'message' : f'cannot stop medialive channel {ChannelId}'
            }

        print(medialive_stop_channel['State'])

        ddb_channel.update_item(
            Key={
                'ChannelId': ChannelId
            },
            UpdateExpression='set #keyState = :State',
            ExpressionAttributeNames={
                '#keyState' : 'State',
            },
            ExpressionAttributeValues={
                ':State': medialive_stop_channel['State']
            }
        )
        response = {
            'message' : f'stopping channel {ChannelId}',
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }
    else :
        response = {
                'message' : 'cannot stop channel - no ChannelId',
            }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }