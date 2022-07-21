import json
import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Key, Attr

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
bucket_name = 'tagsbucket2'

def lambda_handler(event, context):
    # TODO implement
    #event['TagId']
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb', config=my_config)
    
    location = boto3.client('s3').get_bucket_location(Bucket='tagsbucket2')['LocationConstraint']
    

    table = dynamodb.Table('TagsManager')
    event = json.loads(event['body'])
    response = table.scan(FilterExpression=Attr('TagId').contains(event['TagId']))
    data = ''
    for i in range(len(response['Items'])):

        data += "https://s3.amazonaws.com/%s/%s" % (bucket_name, response['Items'][i]['ImageId']) + ',' + ' '
    #data = response['Items'][0]
    print(data)
    

    #while 'LastEvaluatedKey' in response:
    #    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    #    data.extend(response['Items'])
    
 

    return {
        "statusCode": 200,
        "body": json.dumps(str(data)),
        "isBase64Encoded": False,
        "headers": {'Content-Type': 'application/json'}
    }
    