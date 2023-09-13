# copy from one bucket to another using boto3
# https://stackoverflow.com/questions/30161700/move-files-between-two-aws-s3-buckets-using-boto3
import boto3

PUBLIC_BUCKET = "power-rankings-dataset-gprhack"
PRIVATE_BUCKET = "power-ranking"
s3 = boto3.resource('s3')
us_client = boto3.client('s3', region_name='us-west-2')



S3_BUCKET_URL = "https://power-rankings-dataset-gprhack.s3.us-west-2.amazonaws.com"
def move_file(key):
    import boto3
    copy_source = {
        'Bucket': PUBLIC_BUCKET,
        'Key': key
    }
    us_client.copy(copy_source, PRIVATE_BUCKET, key)


public_objects = us_client.list_objects(Bucket='power-rankings-dataset-gprhack')

for object in public_objects['Contents'][:10]:
    obj_key = object["Key"]
    print(obj_key)
    move_file(obj_key)


# Let's use Amazon S3

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
