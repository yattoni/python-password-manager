import base64
import boto3
import json

from Crypto.Random import get_random_bytes
from hashlib import pbkdf2_hmac

def lambda_handler(event, context):
    """
    Lambda function for POST to /signup.
    Checks if account with given username exists or not.
    If does exist, returns 400 error.
    If not, creates new salt for authentication hash, and stores salted hash in new entry in DynamoDB.
    """
    event_body = json.loads(event['body'])
    username = event_body['username']
    auth_hash = event_body['auth_hash']

    dynamo_db_client = boto3.client('dynamodb')
    db_response = dynamo_db_client.get_item(TableName='CS460PwdMngr', Key={'user': {'S': username}})

    if 'Item' in db_response.keys():
        body = dict()
        body['message'] = 'An account with that username already exists.'
        return {
            'statusCode': 400,
            'body': json.dumps(body)
        }
    else:
        salt = get_random_bytes(32)
        decoded_auth_hash = base64.b64decode(auth_hash.encode())
        hash = pbkdf2_hmac('sha256',decoded_auth_hash, salt, 100000, 32)
        dynamo_db_client.put_item(TableName='CS460PwdMngr', Item={'user': {'S': username},
                                                                  'auth_hash': {'B': hash},
                                                                  'salt': {'B': salt}})


    body = dict()
    body['username'] = username
    body['auth_hash'] = auth_hash
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
