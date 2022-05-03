# create_all_buckets.py
import sys
sys.path.insert(0, '../')
from src.util import minio_client as client
from src.util import required_tags, default_tags, alias, policy_set, \
                 policy_directory, get_logger, HOME_PATH
from minio.commonconfig import Tags
import argparse
import json
import os
from bmc._utils import Command
from bmc import admin_policy_set, admin_policy_add, admin_user_add
import random
import string


logger = get_logger('create_buckets')


def create_buckets(bucket_set: dict):
    # check bucket_name exists or not
    bucket_name = bucket_set['bucket_name']
    if client.bucket_exists(bucket_name):
        logger.error('%s already exists, please change the bucket_name',
                     bucket_name)
        return False
    else:
        # make a bucket
        client.make_bucket(bucket_name)
        logger.info('%s is created successfully', bucket_name)

        # change quota limit
        bucket_path = alias + '/' + bucket_name
        quota = int(bucket_set['quota']) * (1024**3)
        if change_quota(target=bucket_path, quota=quota):
            logger.info("%s's quota is set successfully", bucket_name)
        else:
            logger.error("%s's quota is set unsuccessfully", bucket_name)
        # add user
        project_name = bucket_set['project_name']
        password = ''.join(random.choice(string.ascii_letters + string.digits)
                           for x in range(8))
        add_user_response = admin_user_add(target=alias, username=project_name,
                                           password=password)
        if add_user_response.content['status'] == 'success':
            logger.info("User:%s is set successfully", project_name)
        elif add_user_response.content['status'] == 'error':
            logger.error("User:%s is set unsuccessfully",
                         bucket_name)
            return False
        # set policy
        policy_set_cp = policy_set.copy()
        policy_type = bucket_set['permission']
        policy_temp = policy_set_cp[policy_type]
        policy = policy_temp.render(bucket_name=bucket_name)
        policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
        policy_dir = os.path.join(HOME_PATH, policy_directory)
        policy_file_path = policy_dir + policy_name + '.json'
        with open(policy_file_path, 'w') as f:
            json.dump(json.loads(policy), f, ensure_ascii=False)
        set_policy_response = admin_policy_add(target=alias, name=policy_name,
                                               file=policy_file_path)
        if set_policy_response.content['status'] == 'success':
            logger.info("%s's policy is set successfully", bucket_name)
            os.remove(policy_file_path)
            logger.info("%s's policy json file is removed successfully",
                        bucket_name)
        elif set_policy_response.content['status'] == 'error':
            logger.error("%s's policy is set unsuccessfully",
                         bucket_name)
            return False
        # set policy to user
        policy2user_response = admin_policy_set(target=alias, name=policy_name,
                                                user=project_name)
        if policy2user_response.content['status'] == 'success':
            logger.info("Set %s to %s successfully",
                        policy_name, project_name)
        else:
            logger.error("Set %s to %s unsuccessfully",
                         policy_name, project_name)
            return False
        # set tag
        if set_bucket_tags(bucket_set):
            logger.info("%s's tags are set successfully", bucket_name)
        else:
            logger.error("%s's tags are set unsuccessfully", bucket_name)
            return False
        return True


def set_bucket_tags(bucket_set: dict):
    bucket_name = bucket_set['bucket_name']
    tag_to_set = Tags.new_bucket_tags()
    # set required tags by json file
    for tag in required_tags:
        tag_to_set[tag] = bucket_set[tag]
    # set default tags
    for key in default_tags.keys():
        tag_to_set[key] = default_tags[key]
    # set tags
    client.set_bucket_tags(bucket_name, tag_to_set)
    return True


def change_quota(**kwargs):
    cmd = Command('mc {flags} admin bucket quota {target} --hard {quota}')
    response = cmd(**kwargs)
    if response.content['status'] == 'success':
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # get directory of json data by arg
    parser.add_argument("--dir", "-d", type=str, required=True)
    args = parser.parse_args()
    for name in os.listdir(args.dir):
        # concat directory name and name of file
        file_name = os.path.join(args.dir, name)
        with open(file_name) as bucket_data:
            data = json.load(bucket_data)
            bucket_name = data['bucket_name']
            if create_buckets(data):
                logger.info('Finish create and set %s successfully',
                            bucket_name)
            else:
                logger.error('Errors occurs when creating %s or setting of %s',
                             bucket_name, bucket_name)
