# remove_all_buckets.py

from util import minio_client as client
from util import get_logger

logger = get_logger('remove_all_buckets')


def remove_all_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        objs = client.list_objects(bucket.name, recursive=True)
        for obj in objs:
            client.remove_object(object_name=obj.object_name, bucket_name=bucket.name)
        client.remove_bucket(bucket.name)
    logger.info('All buckets are removed successfully')


if __name__ == "__main__":
    remove_all_buckets()
