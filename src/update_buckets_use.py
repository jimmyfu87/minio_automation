# update_buckets_use.py

from bmc import ls
from minio import Minio
import argparse
import json
from minio_client import minio_client
from bmc._utils import Command
from util import use_ratio_threshold_dic, \
                use_ratio_healthy_status_name, get_logger,\
                env_file_dir


logger = get_logger('update_buckets_use')


def get_all_bucket_name(alias: str):
    # get name of all buckets
    bucket_content = ls(target=alias).content
    all_bucket_name = []
    for i in bucket_content:
        # remove last character: '/'
        all_bucket_name.append(i['key'][:-1])
    return all_bucket_name


def get_bucket_usage_cmd(**kwargs):
    cmd = Command('mc {flags} du {target}/{bucket_name}')
    response = cmd(**kwargs)
    if response.content['status'] == 'success':
        bucket_usage = response.content['size']/(1024**3)
    else:
        logger.error('Error occurs when get usage of bucket')
    return bucket_usage


def get_all_bucket_usage_dic(client: Minio, alias: str):
    bucket_usage_dic = {}
    buckets = client.list_buckets()
    for bucket in buckets:
        # sum all object size
        bucket_usage_gib = get_bucket_usage_cmd(target=alias,
                                                bucket_name=bucket.name)
        # set bucket usage dic
        bucket_usage_dic.update({bucket.name: bucket_usage_gib})
    return bucket_usage_dic


def divide_use_ratio_gp(use_ratio: float):
    # sort threshold from big to small
    sort_thres_ls = sorted(use_ratio_threshold_dic.items(),
                           key=lambda x: x[1], reverse=True)
    # if bigger than threshold return status
    for item in sort_thres_ls:
        status = item[0]
        threshold = item[1]
        if use_ratio >= threshold:
            return status
    # if smaller than all threshold return healthy status name
    return use_ratio_healthy_status_name


def get_quota(**kwargs):
    cmd = Command('mc {flags} admin bucket quota {target}/{bucket_name}')
    response = cmd(**kwargs)
    if response.content['status'] == 'success':
        # get quota and transfer to gib
        quota = int(response.content['quota'] / 1024**3)
        return quota
    else:
        logger.error('Error occurs when get_quota')


def update_usage_quota(client: Minio, alias: str):
    bucket_usage_dic = get_all_bucket_usage_dic(client, alias)
    for bucket_name, bucket_usage in bucket_usage_dic.items():
        bucket_tags = client.get_bucket_tags(bucket_name)
        bucket_tags['usage'] = str(bucket_usage)
        bucket_quota_gib = get_quota(target=alias,
                                     bucket_name=bucket_name)
        bucket_tags['quota'] = str(bucket_quota_gib)
        client.set_bucket_tags(bucket_name, bucket_tags)
    return True


def update_use_ratio_status(client: Minio):
    buckets = client.list_buckets()
    for bucket in buckets:
        # get all original bucket tags
        bucket_tags = client.get_bucket_tags(bucket.name)
        # get original usage
        bucket_usage = float(bucket_tags['usage'])
        # get original quota
        bucket_quota = int(bucket_tags['quota'])
        # calculate bucket use_ratio
        bucket_use_ratio = round((bucket_usage / bucket_quota)*100, 1)
        # assign status to bucket
        bucket_status = divide_use_ratio_gp(bucket_use_ratio)
        # set use_ratio and status tags to bucket
        bucket_tags['use_ratio'] = str(bucket_use_ratio)
        bucket_tags['status'] = bucket_status
        client.set_bucket_tags(bucket.name, bucket_tags)
    return True


def update_buckets_use(env_name: str):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    alias = env_data['alias']
    client = minio_client(env_data).get_client()
    if update_usage_quota(client, alias):
        logger.info('Update usage and quota of buckets successfully')
        if update_use_ratio_status(client):
            logger.info('Update use_ratio and status of '
                        'buckets successfully')
            return True
        else:
            logger.error('Update use_ratio and status of '
                         'buckets unsuccessfully')
            return False
    else:
        logger.error('Update usage quota of buckets unsuccessfully')
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", "-e", type=str, required=True)
    args = parser.parse_args()
    if update_buckets_use(args.env):
        logger.info('Update buckets use successfully')
    else:
        logger.error('Update buckets use unsuccessfully')
