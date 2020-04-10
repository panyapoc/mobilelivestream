# API - null
# 1. find idle channel
# 2. start idle channel
# 3. return RMTP endpoint

import boto3
import json
import os

# BOTO3
medialive = boto3.client('medialive')
dynamodb = boto3.resource('dynamodb')

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])

def lambda_handler(event, context):
    ChannelId = json.loads(event['body']).get('ChannelId',False) # ChannelId or False
    if ChannelId :
        try:
            medialive_start_channel = medialive.start_channel(
                ChannelId=ChannelId
            )
        except:
            response = {
                'message' : 'cannot start medialive channel',
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        Channel['State'] = medialive_start_channel['State']
        ddb_channel.update_item(
            Key={
                'ChannelId': ChannelId
            },
            UpdateExpression='set #keyState = :State',
            ExpressionAttributeNames={
                '#keyState' : 'State',
            },
            ExpressionAttributeValues={
                ':State': medialive_start_channel['State']
            }
        )
        response = {
            'message' : f'starting Channel {ChannelId}',
            'ChannelId' : ChannelId
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
        ddb_scan = ddb_channel.scan()
        Channel = {}
        founded = False

        for Item in ddb_scan['Items'] :
            if Item['State'] == 'IDLE' :
                Channel = Item
                founded = True
                break

        if founded :
            ChannelId = Channel['ChannelId']
            try:
                medialive_start_channel = medialive.start_channel(
                    ChannelId=ChannelId
                )
            except:
                response = {
                    'message' : 'cannot start medialive channel',
                }
                return {
                    'statusCode': 200,
                    'body': json.dumps(response)
                }
            Channel['State'] = medialive_start_channel['State']
            ddb_channel.update_item(
                Key={
                    'ChannelId': ChannelId
                },
                UpdateExpression='set #keyState = :State',
                ExpressionAttributeNames={
                    '#keyState' : 'State',
                },
                ExpressionAttributeValues={
                    ':State': medialive_start_channel['State']
                }
            )
            response = {
                'message' : f'starting Channel {ChannelId}',
                'ChannelId' : ChannelId,
                'RTMPendpoint' : Channel['RTMPEndpoint']
            }
        else :
            response = {
                'message' : 'no idle channel please wait',
            }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }


