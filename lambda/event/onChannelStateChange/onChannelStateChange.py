# CloudWatch Channel State Change Event idle -> Running
# 1. Update Channel State on DDB
# 2. Notify Mobile Channel Ready

# CloudWatch Channel State Change Event Running -> Idle
# 1. Update Channel State on DDB
# 2. Start moving archive file to new location
# 3. Create .m3u8 file from list of .ts file
# 4. Add new .m3u8 to DDB for future playing

import boto3
import json
import os

# BOTO3
medialive = boto3.client('medialive')
dynamodb = boto3.resource("dynamodb")

ddb_channel = dynamodb.Table(os.environ['ddb_channel'])

def lambda_handler(event, context):
    # CloudWatch Channel State Change Event idle -> Running
    # 1. Update Channel State on DDB
    # 2. Notify Mobile Channel Ready
    if event['detail']['state'] == Running :
        return 'ok'



    # CloudWatch Channel State Change Event Running -> Idle
    # 1. Update Channel State on DDB
    # 2. Start moving archive file to new location
    # 3. Create .m3u8 file from list of .ts file
    # 4. Add new .m3u8 to DDB for future playing
    elif event['detail']['state'] == Running :
        return 'ok'


    return 'ok'