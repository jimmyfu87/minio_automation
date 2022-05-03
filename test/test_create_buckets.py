# test_create_buckets.py
import sys
sys.path.insert(0, '../')
from src.create_buckets import create_buckets
from src.util import minio_client as client
from src.util import default_tags, required_tags, alias
from bmc._utils import Command
from bmc import admin_policy_info


bucket_data = {
    "bucket_name": "testbucket",
    "project_name": "project1",
    "privacy_ind": "Y",
    "purpose": "model_used",
    "permission": "RW",
    "quota": "30"
}


def get_quota(**kwargs):
    cmd = Command('mc {flags} admin bucket quota {target}/{bucket_name}')
    response = cmd(**kwargs)
    if response.content['status'] == 'success':
        quota = response.content['quota'] / 1024**3
    return quota


def test_create_buckets():
    bucket_name = bucket_data['bucket_name']
    # remove bucket if bucket name already exists
    if client.bucket_exists(bucket_name):
        client.remove_bucket(bucket_name)
    if create_buckets(bucket_data):
        # test bucket is created or not
        assert client.bucket_exists(bucket_name) == True
        tags = client.get_bucket_tags(bucket_name)
        # test tags of bucket
        for key in required_tags:
            assert tags[key] == bucket_data[key]
        for key, value in default_tags.items():
            assert tags[key] == value
        # test quota limit
        bucket_quota_limit = int(get_quota(target=alias,
                                           bucket_name=bucket_name))
        test_bucket_quota_limit = int(bucket_data['quota'])
        assert bucket_quota_limit == test_bucket_quota_limit
        # test policy
        policy_type = bucket_data['permission']
        policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
        response = admin_policy_info(target=alias, name=policy_name)
        assert response.content['status'] == 'success'
