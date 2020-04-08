# API - null
# list Channel: State, Viewing Endpoint

import json
import os
import boto3
import decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
ddb_channel = dynamodb.Table(os.environ["ddb_channel"])

def lambda_handler(event, context):

    response = ddb_channel.scan()
    print('=====response=====')
    print(response)



    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        'body': json.dumps(response['Items'],cls=DecimalEncoder)
    }



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)