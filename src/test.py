# test.py

from update_buckets_use import get_quota
from util import minio_client as client
from bmc import admin_user_info, config_host_list
import subprocess
from util import HOME_PATH, alias, default_tags, required_tags,\
                 get_logger
from create_apply import check_policy_exist, check_user_exist
from os.path import join
import os
import pandas as pd
import json

logger = get_logger('test')
pic_path = 'test_file/test.jpg'
pic_size_gib = os.path.getsize(pic_path) / 1024**3
update_usage = [pic_size_gib, pic_size_gib*10]
update_use_ratio = [pic_size_gib/1, (pic_size_gib*10)/50]
update_status = ['Healthy', 'Healthy']
projects_summary_path = 'test_file/projects_summary.csv'
buckets_summary_path = 'test_file/buckets_summary.csv'


def get_test_apply_set():
    test_apply_sets = []
    for i in range(1, 3, 1):
        file_name = 'test_file/test_json/test_data' + str(i) + '.json'
        with open(file_name) as bucket_data:
            data = json.load(bucket_data)
            test_apply_sets.append(data)
    return test_apply_sets


def get_all_test_buckets_set():
    all_test_buckets_set = []
    for i in range(1, 3, 1):
        file_name = 'test_file/test_json/test_data' + str(i) + '.json'
        with open(file_name) as bucket_data:
            data = json.load(bucket_data)
            project_name = data['project_name']
            if 'bucket' in data.keys():
                for bucket in data['bucket']:
                    bucket_set = bucket
                    bucket_set.update({'project_name': project_name})
                    all_test_buckets_set.append(bucket_set)
    return all_test_buckets_set


def test_add_host():
    alias_exist = False
    response = config_host_list()
    hosts = response.content
    for host in hosts:
        if host['alias'] == alias:
            alias_exist = True
    assert alias_exist is True


def test_create_apply(test_apply_sets):
    for apply_set in test_apply_sets:
        project_name = apply_set['project_name']
        if apply_set['type'] == 'init':
            assert check_user_exist(project_name) is True
        if 'bucket' in apply_set.keys():
            all_buckets = apply_set['bucket']
            for bucket in all_buckets:
                bucket_name = bucket['bucket_name']
                # test bucket is created or not
                assert client.bucket_exists(bucket_name) is True
                # test quota limit
                bucket_quota_limit = int(get_quota(target=alias,
                                                   bucket_name=bucket_name))
                test_bucket_quota_limit = int(bucket['quota'])
                assert bucket_quota_limit == test_bucket_quota_limit
        if 'policy' in apply_set.keys():
            all_policies = apply_set['policy']
            for policy in all_policies:
                # test policy exists
                policy_type = policy['permission']
                policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
                assert check_policy_exist(policy_name) is True
                # test user exists and policy is set
                user_resp = admin_user_info(target=alias,
                                            username=project_name).content
                assert user_resp['status'] == 'success'
                assert 'policyName' in user_resp.keys()
                assert policy_name in user_resp['policyName']
    all_test_buckets_set = get_all_test_buckets_set()
    for bucket_set in all_test_buckets_set:
        # test tags of bucket
        tags = client.get_bucket_tags(bucket_set['bucket_name'])
        for key in required_tags:
            assert tags[key] == bucket_set[key]
        for key, value in default_tags.items():
            assert tags[key] == value
    logger.info('Finish test_create_apply successfully')


def test_update_buckets_use(test_buckets, update_usage,
                            update_use_ratio, update_status):
    for i in range(len(test_buckets)):
        bucket_name = test_buckets[i]['bucket_name']
        tags = client.get_bucket_tags(bucket_name)
        assert tags['usage'] == str(update_usage[i])
        assert tags['use_ratio'] == str(update_use_ratio[i])
        assert tags['status'] == str(update_status[i])
    logger.info('Finish test_update_buckets_use successfully')


def test_projects_summary():
    new_df = pd.read_csv(projects_summary_path)
    correct_df = pd.read_csv('test_file/test_projects_summary.csv')
    pd.testing.assert_frame_equal(new_df, correct_df, check_dtype=True)
    logger.info('Finish test_projects_summary successfully')


def test_buckets_summary():
    new_df = pd.read_csv(buckets_summary_path)
    correct_df = pd.read_csv('test_file/test_buckets_summary.csv')
    new_df.drop(columns=['create_time'], inplace=True)
    correct_df.drop(columns=['create_time'], inplace=True)
    pd.testing.assert_frame_equal(new_df, correct_df, check_dtype=True)
    logger.info('Finish test_buckets_summary successfully')


if __name__ == "__main__":
    # get bucket data from test_file/test_json
    test_apply_sets = get_test_apply_set()
    test_bucket_sets = get_all_test_buckets_set()
    test_json_path = join(HOME_PATH, 'src/test_file/test_json')
    # test command line
    add_host_line = 'python add_host.py'
    create_apply_line = 'python ' + 'create_apply.py' + ' -d ' + test_json_path
    update_buckets_use_line = 'python update_buckets_use.py'
    projects_summary_line = ('python projects_summary.py -f '
                             'test_file/projects_summary')
    buckets_summary_line = ('python buckets_summary.py -f '
                            'test_file/buckets_summary')
    # add host
    resp = subprocess.run(add_host_line, shell=True)
    if resp.returncode == 0:
        # test add_host
        test_add_host()
        # create bucket
        resp = subprocess.run(create_apply_line, shell=True)
        if resp.returncode == 0:
            # test create_apply.py
            test_create_apply(test_apply_sets)
            # put 12 objects
            bucket_name1 = test_apply_sets[0]['bucket'][0]['bucket_name']
            client.fput_object(bucket_name1, "test.jpg", pic_path)
            for i in range(10):
                file_name = str(i) + '.jpg'
                bucket_name2 = test_apply_sets[1]['bucket'][0]['bucket_name']
                client.fput_object(bucket_name2, file_name, pic_path)
            resp = subprocess.run(update_buckets_use_line, shell=True)
            if resp.returncode == 0:
                # test update_buckets_use.py
                test_update_buckets_use(test_bucket_sets, update_usage,
                                        update_use_ratio, update_status)
                resp = subprocess.run(projects_summary_line, shell=True)
                # test_projects_summary
                if resp.returncode == 0:
                    test_projects_summary()
                    os.remove(projects_summary_path)
                    resp = subprocess.run(buckets_summary_line, shell=True)
                    # test_buckets_summary
                    if resp.returncode == 0:
                        test_buckets_summary()
                        os.remove(buckets_summary_path)
                        logger.info('Finish all test successfully')
                    else:
                        logger.error("error:", resp)
            else:
                logger.error("error:", resp)
        else:
            logger.error("error:", resp)
    else:
        logger.error("error:", resp)
