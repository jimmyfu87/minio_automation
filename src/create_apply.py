# create_apply.py

from util import minio_client as client
from util import required_tags, default_tags, alias, policy_temp_set, \
                 policy_directory, get_logger, HOME_PATH, password_len
from minio.commonconfig import Tags
import argparse
import json
import os
from bmc._utils import Command
from bmc import admin_policy_add, admin_user_add,\
                admin_user_info, admin_user_list,\
                admin_policy_list
import random
import string


logger = get_logger('create_apply')


def check_user_exist(username: str):
    users = admin_user_list(target=alias).content
    user_ls = []
    if type(users) == dict:
        user_ls.append(users)
    elif type(users) == list:
        user_ls = users
    username_ls = []
    for user in user_ls:
        username_ls.append(user['accessKey'])
    if username in username_ls:
        return True
    else:
        return False


def check_policy_exist(policy_name: str):
    policies = admin_policy_list(target=alias).content
    policy_ls = []
    if type(policies) == dict:
        policy_ls.append(policies)
    elif type(policies) == list:
        policy_ls = policies
    policy_name_ls = []
    for policy in policy_ls:
        policy_name_ls.append(policy['policy'])
    if policy_name in policy_name_ls:
        return True
    else:
        return False


def create_buckets(apply_set: dict):
    project_name = apply_set['project_name']
    # add user
    add_user_check = False
    if apply_set['type'] == 'init':
        add_user_check = True
    elif apply_set['type'] == 'extend':
        if check_user_exist(project_name):
            logger.info('%s exists', project_name)
        else:
            logger.error('User %s do not exist, please init project',
                         project_name)
            return False
    if add_user_check:
        if add_user(project_name) is False:
            return False
    # make a bucket
    if 'bucket' in apply_set.keys():
        all_buckets = apply_set['bucket']
        for bucket in all_buckets:
            bucket_set = bucket
            bucket_set.update({'project_name': project_name})
            bucket_name = bucket_set['bucket_name']
            quota = bucket_set['quota']
            # check bucket_name exists or not
            if client.bucket_exists(bucket_name):
                logger.error('%s already exists, please change bucket_name',
                             bucket_name)
                return False
            client.make_bucket(bucket_name)
            logger.info('%s is created successfully', bucket_name)
            # change quota limit
            if change_quota(bucket_name, quota) is not True:
                return False
            # set tag
            if set_bucket_tags(bucket_set):
                logger.info("%s's tags are set successfully", bucket_name)
            else:
                logger.error("%s's tags are set unsuccessfully", bucket_name)
                return False
    # add policy and set policy to user
    if 'policy' in apply_set.keys():
        all_policies = apply_set['policy']
        for policy in all_policies:
            policy_set = policy
            # get bucket_name
            bucket_name = policy_set['bucket_name']
            # get policy_type
            policy_type = policy_set['permission']
            # generate policy name ex: 'bucket8_RO_policy'
            policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
            policy_set.update({'project_name': project_name})
            policy_set.update({'policy_name': policy_name})
            if add_policy(policy_set) is not True:
                return False
            if set_policy2user(policy_set) is not True:
                return False
    return True


def change_quota(bucket_name: str, quota: str):
    # change quota limit
    bucket_path = alias + '/' + bucket_name
    quota = int(quota) * (1024**3)
    if change_quota_cmd(target=bucket_path, quota=quota):
        logger.info("%s's quota is set successfully", bucket_name)
        return True
    else:
        logger.error("%s's quota is set unsuccessfully", bucket_name)
        return False


def change_quota_cmd(**kwargs):
    cmd = Command('mc {flags} admin bucket quota {target} --hard {quota}')
    response = cmd(**kwargs)
    if response.content['status'] == 'success':
        return True
    else:
        return False


def add_user(project_name: str):
    username = project_name
    password = ''.join(random.choice(string.ascii_letters + string.digits)
                       for x in range(password_len))
    if check_user_exist(username):
        logger.error("%s already exists, please change the project_name' ",
                     username)
        return False
    add_user_response = admin_user_add(target=alias, username=username,
                                       password=password).content
    if add_user_response['status'] == 'success':
        logger.info("User:%s is set successfully", project_name)
        return True
    elif add_user_response['status'] == 'error':
        logger.error("User:%s is set unsuccessfully",
                     username)
        err_message = add_user_response['error']['message']
        err_cause = add_user_response['error']['cause']['message']
        logger.error('Error Message: ' + err_message)
        logger.error('Error Cause: ' + err_cause)
        return False


def add_policy(policy_set: dict):
    policy_name = policy_set['policy_name']
    if check_policy_exist(policy_name):
        logger.info("%s already exists, do not need to add policy",
                    policy_name)
        return True
    policy_temp_set_cp = policy_temp_set.copy()
    # get_bucket_name
    bucket_name = policy_set['bucket_name']
    # get policy_type
    policy_type = policy_set['permission']
    # get policy template of policy_type
    policy_temp = policy_temp_set_cp[policy_type]
    # change policy template's bucket name
    policy = policy_temp.render(bucket_name=bucket_name)
    # path for policy json
    policy_dir = os.path.join(HOME_PATH, policy_directory)
    policy_file_path = policy_dir + policy_name + '.json'
    # save json file
    with open(policy_file_path, 'w') as f:
        json.dump(json.loads(policy), f, ensure_ascii=False)
    # use json file to add policy
    add_policy_response = admin_policy_add(target=alias,
                                           name=policy_name,
                                           file=policy_file_path).content
    if add_policy_response['status'] == 'success':
        logger.info("%s's policy is set successfully", bucket_name)
        os.remove(policy_file_path)
        logger.info("%s's policy json file is removed successfully",
                    bucket_name)
        return True

    elif add_policy_response['status'] == 'error':
        logger.error("%s's policy is set unsuccessfully",
                     bucket_name)
        err_message = add_policy_response['error']['message']
        err_cause = add_policy_response['error']['cause']['message']
        logger.error('Error Message: ' + err_message)
        logger.error('Error Cause: ' + err_cause)
        return False


def set_policy2user(policy_set: dict):
    project_name = policy_set['project_name']
    policy_name = policy_set['policy_name']
    user_response = admin_user_info(target=alias,
                                    username=project_name).content
    all_policy = [policy_name]
    if user_response['status'] == 'success':
        # get original policy and add to all policy
        if 'policyName' in user_response.keys():
            logger.info("%s has original policy",
                        project_name)
            original_policy = user_response['policyName']
            all_policy.append(original_policy)
        else:
            logger.info("%s has no original policy",
                        project_name)
    policy2user_response = set_policy2user_cmd(target=alias,
                                               policy=all_policy,
                                               user=project_name).content
    if policy2user_response['status'] == 'success':
        logger.info("Set %s to %s successfully",
                    policy_name, project_name)
        return True
    else:
        logger.error("Set %s to %s unsuccessfully",
                     policy_name, project_name)
        err_message = policy2user_response['error']['message']
        err_cause = policy2user_response['error']['cause']['message']
        logger.error('Error Message: ' + err_message)
        logger.error('Error Cause: ' + err_cause)
        return False


def set_policy2user_cmd(target, policy, user):
    policy_ls = ','.join(policy)
    cmd_line = 'mc {flags} admin policy set ' + \
               target + ' ' + policy_ls + ' user=' + user
    cmd = Command(cmd_line)
    return cmd()


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # get directory of json data by arg
    parser.add_argument("--dir", "-d", type=str, required=True)
    args = parser.parse_args()
    for name in os.listdir(args.dir):
        # concat directory name and name of file
        file_name = os.path.join(args.dir, name)
        with open(file_name) as apply_data:
            data = json.load(apply_data)
            if create_buckets(data):
                logger.info('Finish create and set %s successfully',
                            file_name)
            else:
                logger.error('Errors occurs when creating or setting of %s',
                             file_name)
