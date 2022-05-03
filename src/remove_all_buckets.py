# remove_all_buckets.py
import sys
sys.path.insert(0, '../')
from src.util import minio_client as client
from src.util import get_logger

logger = get_logger('remove_all_buckets')


def remove_all_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        client.remove_bucket(bucket.name)
    logger.info('All buckets are removed successfully')


if __name__ == "__main__":
    remove_all_buckets()
