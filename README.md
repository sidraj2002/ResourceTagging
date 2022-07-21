# ResourceTagging


![Alt text](https://github.com/sidraj2002/ResourceTagging/blob/main/ImageTagging.png)



AWS Resources:

DDB Table: 
TagManager Table
ImageID | TagId | Metadata

Lambda Functions:
TagManagerLambda01 -> Fetch event from APIGateway -> Query DDB Table

S3Bucket:
tagsbucket2 -> Store Images

IAM:
Lambdaexectution role -> DDB permissions

CloudWatch:
Logstream-> TagsManagerAPI -> APIGateway