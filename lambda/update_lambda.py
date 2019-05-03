import base64
import boto3
import json

from hashlib import pbkdf2_hmac

def lambda_handler(event, context):
    """
    Lambda function for POST to /update.
    Authenticates account using authentication hash and salted hash stored in DynamoDB.
    If hashes match, update encrypted vault in DynamoDB with one from request body.
    """
    event_body = json.loads(event['body'])
    username = event_body['username']
    auth_hash = event_body['auth_hash']
    vault = event_body['vault']

    dynamo_db_client = boto3.client('dynamodb')
    db_response = dynamo_db_client.get_item(TableName='CS460PwdMngr', Key={'user': {'S': username}})

    if 'Item' not in db_response.keys():
        body = dict()
        body['message'] = 'Auth failed.'
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
            body['message'] = 'Auth failed.'
            return {
                'statusCode': 400,
                'body': json.dumps(body)
            }
        dynamo_db_client.put_item(TableName='CS460PwdMngr', Item={'user': {'S': username},
                                                                  'auth_hash': {'B': stored_hash},
                                                                  'salt': {'B': stored_salt},
                                                                  'vault': {'S': vault}})

    body = dict()
    body['message'] = 'Success!'
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
