# update_usage.py
import bmc
from util import minio_client as client
from bmc._utils import Command
from util import use_ratio_threshold_dic, \
                use_ratio_healthy_status_name, alias, get_logger


logger = get_logger('update_buckets_use')


def get_all_bucket_name():
    # get name of all buckets
    bucket_content = bmc.ls(target=alias).content
    all_bucket_name = []
    for i in bucket_content:
        all_bucket_name.append(i['key'][:-1])
    return all_bucket_name


def get_all_bucket_usage_dic():
    bucket_usage_dic = {}
    buckets = client.list_buckets()
    for bucket in buckets:
        # get buck path name
        path = alias + '/' + bucket.name
        # sum all object size
        bucket_usage = get_bucket_usage(path)
        # transfer Byte to Gib
        bucket_usage_gib = bucket_usage / (1024**3)
        # set bucket usage dic
        bucket_usage_dic.update({bucket.name: bucket_usage_gib})
    return bucket_usage_dic


def get_bucket_usage(path: str):
    object_content = bmc.ls(target=path).content
    bucket_usage = 0
    # if there is only one element in response
    if type(object_content) == dict:
        object_content = [object_content]
    for object_item in object_content:
        if object_item['type'] == 'file':
            bucket_usage = bucket_usage + object_item['size']
        # Get folder file recursively
        elif object_item['type'] == 'folder':
            folder_path = path + '/' + object_item['key'][:-1]
            bucket_usage = bucket_usage + get_bucket_usage(folder_path)
    return bucket_usage


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
    cmd = Command('mc {flags} admin bucket quota {alias}/{bucket_name}')
    return cmd(**kwargs)


def update_usage_quota():
    bucket_usage_dic = get_all_bucket_usage_dic()
    for bucket_name, bucket_usage in bucket_usage_dic.items():
        bucket_tags = client.get_bucket_tags(bucket_name)
        bucket_tags['usage'] = str(bucket_usage)
        bucket_quota = get_quota(alias=alias,
                                 bucket_name=bucket_name).content['quota']
        bucket_quota_gib = bucket_quota / (1024**3)
        bucket_tags['quota'] = str(int(bucket_quota_gib))
        client.set_bucket_tags(bucket_name, bucket_tags)
    return True


def update_use_ratio_status():
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
        # set use_ratio and status tags to bucket
        bucket_tags['use_ratio'] = str(bucket_use_ratio)
        bucket_tags['status'] = bucket_status
        client.set_bucket_tags(bucket.name, bucket_tags)
    return True


if __name__ == "__main__":
    if update_usage_quota():
        logger.info('Update usage of buckets successfully')
        if update_use_ratio_status():
            logger.info('Update usage ratio and status of \
                         buckets successfully')
