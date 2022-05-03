# test_update_buckets_use.py
from curses.panel import update_panels
import sys
sys.path.insert(0, '../')
from src.update_buckets_use import divide_use_ratio_gp, update_usage_quota,get_quota
from src.util import alias
from src.util import minio_client as client

def test_divide_use_ratio_gp():
    assert divide_use_ratio_gp(0) == 'Healthy'
    assert divide_use_ratio_gp(0.001) == 'Healthy'
    assert divide_use_ratio_gp(0.15) == 'Aware'
    assert divide_use_ratio_gp(0.4) == 'Cautious'
    assert divide_use_ratio_gp(0.5) == 'Cautious'
    assert divide_use_ratio_gp(0.61) == 'Cautious'
    assert divide_use_ratio_gp(0.9) == 'Danger'
    assert divide_use_ratio_gp(1) == 'Danger'

def test_update_usage_quota():
    if update_usage_quota:
        buckets = client.list_buckets()
        for bucket in buckets:
            tags = client.get_bucket_tags(bucket.name)
            # the quota in tag
            tags_quota_gib = int(tags['quota'])
            # the really quota
            bucket_quota = int(get_quota(alias=alias,
                                    bucket_name=bucket.name).content['quota'])
            bucket_quota_gib = bucket_quota / 1024**3
            assert tags_quota_gib == bucket_quota_gib

def test_update_use_ratio_status():
    buckets = client.list_buckets()
    for bucket in buckets:
        # get all original bucket tags
        bucket_tags = client.get_bucket_tags(bucket.name)
        # get original usage
        bucket_usage = float(bucket_tags['usage'])
        # get original quota
        bucket_quota = int(bucket_tags['quota'])
        # calculate bucket use_ratio
        bucket_use_ratio = int(bucket_usage / bucket_quota)
        # assign status to bucket
        bucket_status = divide_use_ratio_gp(bucket_use_ratio)
        assert bucket_tags['use_ratio'] == str(bucket_use_ratio)
        assert bucket_tags['status'] == bucket_status