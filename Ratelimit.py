from botocore.config import Config
from datetime import datetime, timedelta
import os
import boto3

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

sampleRequest = {
    "requestId": "V1-l3i3EIAMEJeA=",
    "ip": "108.209.197.142",
    "requestTime": "25/Jul/2022:21:55:36 +0000",
    "httpMethod": "GET",
    "routeKey": "GET /PullTag",
    "status": "200",
    "protocol": "HTTP/1.1",
    "responseLength": "803"
}

class requesterId():
    
    def __init__(self):
        self.ipAddr = ''
        self.routeKey = ''
        self.requestTime = ''
    def isNewRequester(self, request, TableName):
        dynamodb = boto3.resource('dynamodb',config=my_config)
        table = dynamodb.Table(TableName)
        checkEntry = table.get_item(Key={'ipaddr':request['ip'], 'timestamp':request['requestTime']})
        #print(checkEntry)
        if 'Item' in checkEntry:
            return False
        else:
            return True
        #if checkEntry['Item']['ipaddr'] ==
    def insertNewRequest(self, Item, TableName):
         dynamodb = boto3.resource('dynamodb',config=my_config)
         table = dynamodb.Table(TableName)
         table.put_item(Item=Item)
        #table.put_item(Item=Item)
   
class throttler():
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.isThrottled = False
        self.windowCounter = 0
        self.requestStruct = {}
        
    def is_ratelimited(self, request):
        struct = {}
        
        if request != None: 
            self.requestStruct = {sampleRequest['ip']:{sampleRequest['routeKey']:sampleRequest['requestTime']}}
            print(self.requestStruct)
            print(datetime.now())

OnRequest = throttler()
OnRequest.is_ratelimited(sampleRequest)

newrequest = requesterId()

if newrequest.isNewRequester(sampleRequest, 'RateLimiter01') == True:
    Item = {'ipaddr':sampleRequest['ip'], 'timestamp':sampleRequest['requestTime'], 'routeKey':sampleRequest['routeKey']}
    newrequest.insertNewRequest(Item, 'RateLimiter01')
else:
    print('Request registered already')