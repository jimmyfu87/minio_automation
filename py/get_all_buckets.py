## get_all_buckets.py

import util

client = util.minio_client


def get_all_buckets():
    buckets = client.list_buckets();
    for bucket in buckets:
        print(bucket.name);
    return buckets


if __name__== "__main__" :
    get_all_buckets();