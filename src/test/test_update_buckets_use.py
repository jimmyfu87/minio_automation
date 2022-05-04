# test_update_buckets_use.py

import sys
sys.path.insert(0, '../')
from update_buckets_use import *         
from util import alias
from util import minio_client as client

bucket_data = {
    "bucket_name": "testbucket",
    "project_name": "project1",
    "privacy_ind": "Y",
    "purpose": "model_used",
    "permission": "RW",
    "quota": "30"
}


def test_get_all_bucket_name():
    assert type(get_all_bucket_name()) == list


def test_get_all_bucket_usage_dic():
    assert type(get_all_bucket_usage_dic()) == dict


def test_get_all_bucket_usage():
    buckets = client.list_buckets()
    for bucket in buckets:
        path = alias + '/' + bucket.name
        assert type(get_bucket_usage(path)) == int or float
        return


def test_divide_use_ratio_gp():
    assert divide_use_ratio_gp(0) == 'Healthy'
    assert divide_use_ratio_gp(0.001) == 'Healthy'
    assert divide_use_ratio_gp(0.15) == 'Aware'
    assert divide_use_ratio_gp(0.4) == 'Cautious'
    assert divide_use_ratio_gp(0.5) == 'Cautious'
    assert divide_use_ratio_gp(0.61) == 'Cautious'
    assert divide_use_ratio_gp(0.9) == 'Danger'
    assert divide_use_ratio_gp(1) == 'Danger'


def test_get_quota():
    buckets = client.list_buckets()
    for bucket in buckets:
        quota = get_quota(target=alias, bucket_name=bucket.name)
        assert quota > 0
        assert type(quota) == int
        return


def test_update_usage_quota():
    if update_usage_quota():
        buckets = client.list_buckets()
        for bucket in buckets:
            tags = client.get_bucket_tags(bucket.name)
            # the quota in tag
            tags_quota_gib = int(tags['quota'])
            # the really quota
            bucket_quota_gib = get_quota(target=alias,
                                         bucket_name=bucket.name)
            assert tags_quota_gib == bucket_quota_gib
            return


def test_update_use_ratio_status():
    if update_use_ratio_status():
        buckets = client.list_buckets()
        for bucket in buckets:
            # get all original bucket tags
            bucket_tags = client.get_bucket_tags(bucket.name)
            # get original usage
            bucket_usage = float(bucket_tags['usage'])
            # get original quota
            bucket_quota = int(bucket_tags['quota'])
            # calculate bucket use_ratio
            bucket_use_ratio = bucket_usage / bucket_quota
            # assign status to bucket
            bucket_status = divide_use_ratio_gp(bucket_use_ratio)
            assert bucket_tags['use_ratio'] == str(bucket_use_ratio)
            assert bucket_tags['status'] == bucket_status
