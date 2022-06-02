# export_minio.py

from util import get_logger, env_file_dir
import argparse
import json
from minio_client import minio_client
from bmc import admin_policy_info, admin_policy_list,\
                admin_user_list
from os.path import join
from update_buckets_use import get_quota

logger = get_logger('export_minio')
export_data_path = '../export_data'
export_policy_path = join(export_data_path, 'policy')


def export_policies(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    alias = env_data['alias']
    policy_ls = admin_policy_list(target=alias).content
    for policy in policy_ls:
        policy_name = policy['policy']
        policy_info = admin_policy_info(
                      target='Staging',
                      name=policy_name).content['policyInfo']['Policy']
        policy_file_path = join(export_policy_path, policy_name) + '.json'
        with open(policy_file_path, 'w') as f:
            json.dump(policy_info, f, ensure_ascii=False)
    return True


def export_users(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    alias = env_data['alias']
    users = admin_user_list(target=alias).content
    user_ls = []
    user_json = []
    if type(users) == dict:
        user_ls.append(users)
    elif type(users) == list:
        user_ls = users
    for user in user_ls:
        user_policy = []
        if 'policyName' in user:
            user_policy = user['policyName'].split(',')
        data = {'access_key': user['accessKey'], 'secret_key': '', 'policy_name': user_policy}
        user_json.append(data)
    user_file_path = join(export_data_path, 'user_ls') + '.json'
    with open(user_file_path, 'w') as f:
        json.dump(user_json, f, ensure_ascii=False)
        return True


def export_buckets(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
    alias = env_data['alias']
    client = minio_client(env_data).get_client()
    buckets = client.list_buckets()
    bucket_json_ls = []
    for bucket in buckets:
        bucket_name = bucket.name
        unassign = 'Unassigned'
        bucket_json = {
                        'bucket_name': bucket_name,
                        'project_name': unassign,
                        'management_unit': unassign,
                        "privacy_ind": unassign,
                        "purpose": unassign,
                        "save_type": unassign,
                        "quota": unassign,
                        "usage": '0',
                        "use_ratio": '0',
                        "status": 'Healthy',
                      }
        # set bucket tag
        bucket_tag = client.get_bucket_tags(bucket_name)
        for key, value in bucket_tag.items():
            if key == 'project':
                bucket_json.update({'project_name': value})
            bucket_json.update({key: value})
        # get bucket quota
        bucket_quota_gib = get_quota(target=alias,
                                     bucket_name=bucket_name)
        # set bucket quota as a tag
        bucket_json.update({'quota': str(bucket_quota_gib)})
        bucket_json_ls.append(bucket_json)
    bucket_file_path = join(export_data_path, 'bucket_ls') + '.json'
    with open(bucket_file_path, 'w') as f:
        json.dump(bucket_json_ls, f, ensure_ascii=False)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", "-e", type=str, required=True)
    args = parser.parse_args()
    if export_policies(args.env):
        logger.info('policies are exported successfully')
    else:
        logger.error('policies are exported successfully')
    if export_users(args.env):
        logger.info('users are exported successfully')
    else:
        logger.error('users are exported unsuccessfully')
    if export_buckets(args.env):
        logger.info('buckets are exported successfully')
    else:
        logger.error('buckets are exported unsuccessfully')
