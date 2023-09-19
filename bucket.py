# copy from one bucket to another using boto3
# https://stackoverflow.com/questions/30161700/move-files-between-two-aws-s3-buckets-using-boto3
import boto3
import requests

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


def download_ddl_files():
    public_objects = us_client.list_objects(Bucket='power-rankings-dataset-gprhack', Prefix='athena-ready/ddl')

    for object in public_objects['Contents'][:10]:
        obj_key = object["Key"]
        print(obj_key)
        S3_BUCKET_URL = "https://power-rankings-dataset-gprhack.s3.us-west-2.amazonaws.com"

        response = requests.get(f"{S3_BUCKET_URL}/{obj_key}")
        if response.status_code == 200:
            with open(f"{obj_key.split('/')[-1]}", 'wb') as output_file:
                output_file.write(response.content)

download_ddl_files()
# Let's use Amazon S3

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)
