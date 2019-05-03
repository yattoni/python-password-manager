import base64
import boto3
import json

from hashlib import pbkdf2_hmac

def lambda_handler(event, context):
    """
    Lambda function for POST to /login.
    Checks if account with given username exists or not.
    If does not exist, returns 400 error.
    If found, check authentication hash to see if matches hash in DynamoDB using salt.
    If hashes match return encrypted vault.
    """
    event_body = json.loads(event['body'])
    username = event_body['username']
    auth_hash = event_body['auth_hash']

    dynamo_db_client = boto3.client('dynamodb')
    db_response = dynamo_db_client.get_item(TableName='CS460PwdMngr', Key={'user': {'S': username}})

    if 'Item' not in db_response.keys():
        body = dict()
        body['message'] = 'Login failed.'
        return {
            'statusCode': 400,
            'body': json.dumps(body)
        }
    else:
        stored_hash = db_response['Item']['auth_hash']['B']
        stored_salt = db_response['Item']['salt']['B']
        decoded_auth_hash = base64.b64decode(auth_hash.encode())
        hash = pbkdf2_hmac('sha256', decoded_auth_hash, stored_salt, 100000, 32)
        print(stored_hash)
        print(hash)
        if hash != stored_hash:
            body = dict()
            body['message'] = 'Login failed.'
            return {
                'statusCode': 400,
                'body': json.dumps(body)
            }

    body = dict()
    body['vault'] = db_response['Item']['vault']['S']
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
