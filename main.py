import datetime
from PIL import Image
from PIL.ExifTags import TAGS

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

image = MyImg("firstImage")
image.CreateImg("/home/ec2-user/environment/Tags/ResourceTagging/dog.jpg")
