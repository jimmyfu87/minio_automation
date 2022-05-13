# remove_all_buckets.py

from util import get_logger
from minio import Minio

logger = get_logger('remove_all_buckets')

client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)


def remove_all_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        objs = client.list_objects(bucket.name, recursive=True)
        for obj in objs:
            client.remove_object(object_name=obj.object_name,
                                 bucket_name=bucket.name)
        client.remove_bucket(bucket.name)
    logger.info('All buckets are removed successfully')


if __name__ == "__main__":
    remove_all_buckets()
