# API - null
# 1. find idle channel
# 2. start idle channel
# 3. return RMTP endpoint

import boto3
import json
import os

# BOTO3
medialive = boto3.client('medialive')
dynamodb = boto3.resource("dynamodb")

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])

def lambda_handler(event, context):
    ddb_scan = ddb_channel.scan()

    Channel = {}
    founded = False

    for Item in ddb_scan['Items'] :
        if Item['State'] == 'IDLE' :
            Channel = Item
            founded = True
            break

    if founded :
        ChannelID = Channel['ChannelID']
        try:
            medialive_start_channel = medialive.start_channel(
                ChannelId=ChannelID
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
        ddb_channel.put_item(Item=Channel)
        response = {
            'message' : f'starting Channel {ChannelID}',
            'ChannelID' : ChannelID,
            'RTMPendpoint' : Channel['RTMPEndpoint']
        }
    else :
        response = {
            'message' : 'no idle channel please wait',
        }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


