import util
import logging

client = util.minio_client

json_data = {
    "bucket_name": "airflow-logs",
    "project_name": "etl-teams",
    "privacy_ind": 'Y',
    "purpose": 'prject_used',
    "permission": 'RO',  
    "quota" : 10
}

def create_buckets(bucket_name: str, project_name: str, privacy_ind: str, purpose: str, permission: str, quota: int ):
    # Create bucket.
    if client.bucket_exists(bucket_name):
        print('This bucket_name already exists')
    else:
        client.make_bucket(bucket_name)
    
    buckets = client.list_buckets();
    for bucket in buckets:
        print(bucket.name);
    return buckets


if __name__== "__main__" :
    create_buckets();