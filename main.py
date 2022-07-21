import datetime
import logging
import boto3
import secrets
import os
from botocore.exceptions import ClientError

from PIL import Image
from PIL.ExifTags import TAGS

from botocore.config import Config

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

class MyImg:
    imageId = None
    def __init__(self):
        self.imageId = ''
        self.timestamp = datetime.datetime.now()
        self.userId = ''
        self.flag = ''
        self.url = ''
        self.metadata = ''
    def CreateImg(self, ImgPath):
        image = Image.open(ImgPath)
        info_dict = {
             "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
            }
        self.metadata = info_dict
        #print(self.metadata)

def ImgIdGenerator():
    return secrets.token_hex(10)

def S3Uploader(ImgPath, S3BucketName, FileName, object_name=None):
    if object_name is None:
        object_name = os.path.basename(FileName)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(ImgPath, S3BucketName, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
def DynamoUpdate(TableName, Item):
    dynamodb = boto3.resource('dynamodb',config=my_config)
    table = dynamodb.Table(TableName)
    table.put_item(Item=Item)

def TagGenerator(S3Bucket, ObjectName):
    rekognition = boto3.client('rekognition', config=my_config)
    response = rekognition.detect_labels(
    Image={
        'S3Object': {
            'Bucket': S3Bucket,
            'Name': ObjectName,
        },
    },
    MaxLabels=123,
    MinConfidence=95,
    )
    print(response)
    hashtags = ''
    for i in range(len(response['Labels'])):
        hashtags += '#' + response['Labels'][i]['Name']
    hashtags = hashtags.replace(' ', '')
    return hashtags

    

''' Main execution '''
myPath = '/home/ec2-user/environment//Tags/ResourceTagging/Images'

for files in os.listdir(myPath):
    f = os.path.join(myPath, files)
    if os.path.isfile(f):
        image = MyImg()
        image.CreateImg(f)
        image.imageId = ImgIdGenerator() + files
        S3Uploader(f, 'tagsbucket2', image.imageId)
        hashtags = TagGenerator('tagsbucket2', image.imageId)
        if hashtags == None or hashtags == '':
            item = {'ImageId':image.imageId, 'TagId':'#', 'metadata':image.metadata}
        else:
            item = {'ImageId':image.imageId, 'TagId':hashtags, 'metadata':image.metadata}
        #print(item)
        DynamoUpdate('TagsManager', item)
#image = MyImg()
#image.CreateImg("/home/ec2-user/environment/Tags/ResourceTagging/dog.jpg")
#image.imageId = ImgIdGenerator() + 'dog.jpg'

#S3Uploader("/home/ec2-user/environment/Tags/ResourceTagging/dog.jpg", "tagsbucket2", image.imageId)
#RekognitionResponse = TagGenerator('tagsbucket2',image.imageId)
#print(RekognitionResponse)

#item = {'ImageId':image.imageId, 'TagId':RekognitionResponse, 'metadata':image.metadata}
#DynamoUpdate('TagsManager', item)
