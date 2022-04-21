## remove_all_buckets.py

import logging
from util import minio_client


client = minio_client

def remove_all_buckets():
    buckets = client.list_buckets()
    for bucket in buckets:
        client.remove_bucket(bucket.name)
    print('All buckets are removed successfully')
    

if __name__== "__main__" :
    remove_all_buckets()

