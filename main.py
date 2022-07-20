import datetime
import logging
import boto3
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
    def __init__(self, imageId):
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
        print(self.metadata)

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
    


image = MyImg("firstImage")
image.CreateImg("/home/ec2-user/environment/Tags/ResourceTagging/dog.jpg")
S3Uploader("/home/ec2-user/environment/Tags/ResourceTagging/dog.jpg", "tagsbucket2", "dog.jpg")
item = {'ImageId':'imgxxx02', 'TagId':'#dog', 'metadata':image.metadata}
DynamoUpdate('TagsManager', item)
