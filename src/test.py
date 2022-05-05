import sys
sys.path.insert(0, '../')
sys.path.append('../src')
from update_buckets_use import get_quota
from util import minio_client as client
from bmc import admin_policy_info, admin_user_info
import subprocess
from util import HOME_PATH, alias, default_tags, required_tags
from os.path import join
import os
import pandas as pd 

test_buckets = [
                {
                    "bucket_name": "testbucket1",
                    "project_name": "project1",
                    "privacy_ind": "Y",
                    "purpose": "model_used",
                    "permission": "RW",
                    "quota": "1"
                },
                {
                    "bucket_name": "testbucket2",
                    "project_name": "project1",
                    "privacy_ind": "N",
                    "purpose": "model_used",
                    "permission": "RO",
                    "quota" : "50"
                }
]
pic_path = 'test_folder/test_file/1.jpg'
pic_size_gib = os.path.getsize(pic_path) / 1024**3
update_usage = [pic_size_gib, pic_size_gib*10]
update_use_ratio = [pic_size_gib/1, (pic_size_gib*10)/50]
update_status = ['Healthy', 'Healthy']
projects_summary_path = 'test_folder/projects_summary.csv'
buckets_summary_path = 'test_folder/buckets_summary.csv'



def test_create_buckets(test_buckets):
    for bucket in test_buckets:
        bucket_name = bucket['bucket_name']
        project_name = bucket['project_name']
        # test bucket is created or not
        assert client.bucket_exists(bucket_name) == True
        # test quota limit
        bucket_quota_limit = int(get_quota(target=alias,
                                           bucket_name=bucket_name))
        test_bucket_quota_limit = int(bucket['quota'])
        assert bucket_quota_limit == test_bucket_quota_limit
        # test policy exists
        policy_type = bucket['permission']
        policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
        policy_resp = admin_policy_info(target=alias, name=policy_name).content
        assert policy_resp['status'] == 'success'
        # test user exists and policy is set
        user_resp = admin_user_info(target=alias, username=project_name).content
        assert user_resp['status'] == 'success'
        assert 'policyName' in user_resp.keys()
        assert policy_name in user_resp['policyName']
        # test policy exists
        policy_type = bucket['permission']
        policy_name = bucket_name + '_' + policy_type + '_' + 'policy'
        policy_resp = admin_policy_info(target=alias, name=policy_name).content
        assert policy_resp['status'] == 'success'
        # test tags of bucket
        tags = client.get_bucket_tags(bucket_name)
        for key in required_tags:
            assert tags[key] == bucket[key]
        for key, value in default_tags.items():
            assert tags[key] == value


def test_update_buckets_use(test_buckets, update_usage, update_use_ratio, update_status):
    for i in range(len(test_buckets)):
        bucket = test_buckets[i]
        bucket_name = bucket['bucket_name']
        tags = client.get_bucket_tags(bucket_name)
        assert tags['usage'] == str(update_usage[i])
        assert tags['use_ratio'] == str(update_use_ratio[i])
        assert tags['status'] == str(update_status[i])


def test_projects_summary():
    new_df = pd.read_csv(projects_summary_path)
    correct_df =  pd.read_csv('test_folder/test_file/test_projects_summary.csv')
    pd.testing.assert_frame_equal(new_df, correct_df, check_dtype=True)


def test_buckets_summary():
    new_df = pd.read_csv(buckets_summary_path)
    correct_df =  pd.read_csv('test_folder/test_file/test_buckets_summary.csv')
    new_df.drop(columns=['create_time'], inplace=True)
    correct_df.drop(columns=['create_time'], inplace=True)
    pd.testing.assert_frame_equal(new_df, correct_df, check_dtype=True)


if __name__ == "__main__":
    test_json_path = join(HOME_PATH, 'src/test_folder/test_json')
    create_bucket_line= 'python ' + 'create_buckets.py' + ' -d ' + test_json_path
    update_buckets_use_line = 'python update_buckets_use.py'
    projects_summary_line = 'python projects_summary.py -f test_folder/projects_summary'
    buckets_summary_line = 'python buckets_summary.py -f test_folder/buckets_summary'
    # create bucket
    resp = subprocess.run(create_bucket_line, shell=True)
    if resp.returncode == 0:
        # test create_buckets.py
        test_create_buckets(test_buckets)
        # put 12 objects
        client.fput_object(test_buckets[0]['bucket_name'], "1.jpg", "test_folder/test_file/1.jpg")
        for i in range(10):
            file_name = str(i) + '.jpg'
            client.fput_object(test_buckets[1]['bucket_name'], file_name, "test_folder/test_file/1.jpg")
        resp = subprocess.run(update_buckets_use_line, shell=True)
        if resp.returncode == 0:
            # test update_buckets_use.py
            test_update_buckets_use(test_buckets, update_usage, update_use_ratio, update_status)
            resp = subprocess.run(projects_summary_line, shell=True)
            if resp.returncode == 0:
                test_projects_summary()
                os.remove(projects_summary_path)
                resp = subprocess.run(buckets_summary_line, shell=True)
                if resp.returncode == 0:
                    test_buckets_summary()
                    os.remove(buckets_summary_path)
                    print('Finish all test successfully')
                else:
                    print("error:",resp)
        else:
            print("error:",resp)
    else:
        print("error:",resp)





    
