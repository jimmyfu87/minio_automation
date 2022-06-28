# export_minio.py

import argparse
import json
import os
from os.path import join

from bmc import (admin_policy_add, admin_user_add)

from create_apply import change_quota, set_bucket_tags, set_policy2user_cmd
from minio_client import minio_client
from util import env_file_dir, get_logger

logger = get_logger('import_minio')
export_data_path = '../export_data'
export_policy_path = join(export_data_path, 'policy')


def import_policies(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    alias = env_data['alias']
    for file_name in os.listdir(export_policy_path):
        policy_file_path = join(export_policy_path, file_name)
        policy_name = file_name.replace('.json', '')
        resp = admin_policy_add(target=alias,
                                name=policy_name,
                                file=policy_file_path).content
        if resp['status'] == 'success':
            logger.info("%s is added successfully", policy_name)
        else:
            logger.error("%s is added unsuccessfully", policy_name)
            return False
    return True


def import_users(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    user_file_path = join(export_data_path, 'user_ls') + '.json'
    alias = env_data['alias']
    with open(user_file_path) as user_json:
        users = json.load(user_json)
    for user in users:
        username = user['access_key']
        password = user['secret_key']
        # add user
        resp = admin_user_add(target=alias, username=username,
                              password=password).content
        if resp['status'] == 'success':
            logger.info("%s is added successfully", username)
        else:
            logger.error("%s is added unsuccessfully", username)
            return False
        # set policy to user
        user_policies = user['policy_name']
        policy2user_response = set_policy2user_cmd(target=alias,
                                                   policy=user_policies,
                                                   user=username).content
        if policy2user_response['status'] == 'success':
            logger.info("Set %s to %s successfully",
                        user_policies, username)
        else:
            logger.error("Set %s to %s unsuccessfully",
                         user_policies, username)
            err_message = policy2user_response['error']['message']
            err_cause = policy2user_response['error']['cause']['message']
            logger.error('Error Message: ' + err_message)
            logger.error('Error Cause: ' + err_cause)
            return False
    return True


def import_buckets(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    bucket_file_path = join(export_data_path, 'bucket_ls') + '.json'
    alias = env_data['alias']
    client = minio_client(env_data).get_client()
    # make buckets and set tags
    with open(bucket_file_path) as bucket_json:
        buckets = json.load(bucket_json)
    for bucket in buckets:
        bucket_name = bucket['bucket_name']
        quota = bucket['quota']
        client.make_bucket(bucket_name)
        change_quota(bucket_name, quota, alias)
        if set_bucket_tags(bucket, client):
            logger.info("%s's tags are set successfully", bucket_name)
        else:
            logger.error("%s's tags are set unsuccessfully", bucket_name)
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", "-e", type=str, required=True)
    args = parser.parse_args()
    if import_buckets(args.env):
        logger.info('buckets are imported successfully')
        if import_policies(args.env):
            logger.info('policies are imported successfully')
            if import_users(args.env):
                logger.info('users are imported successfully')
            else:
                logger.error('users are imported unsuccessfully')
        else:
            logger.error('policies are imported successfully')
    else:
        logger.error('buckets are imported unsuccessfully')
