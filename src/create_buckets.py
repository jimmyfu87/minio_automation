## create_all_buckets.py

from util import minio_client as client
from util import add_host, required_tags,  default_tags, alias, policy_set, get_logger
from minio.commonconfig import Tags
import argparse
import json
import os
from bmc._utils import Command
import json

logger = get_logger('create_buckets')

def create_buckets(bucket_set: dict):
    # check bucket_name exists or not
    bucket_name = bucket_set['bucket_name']
    if client.bucket_exists(bucket_name):
        logger.error('%s already exists, please change the bucket_name', bucket_name)
        return False
    else:
        # make a bucket
        client.make_bucket(bucket_name)
        logger.info('%s is created successfully', bucket_name)

        # change quota limit
        bucket_path = alias + '/' + bucket_name
        quota = int(bucket_set['quota']) * (1024**3)
        change_quota(target = bucket_path, quota = quota)
        logger.info("%s's quota is set successfully", bucket_name)

        # set policy
        policy_set_cp = policy_set.copy()
        policy = policy_set_cp[bucket_set['permission']]
        policy["Statement"][0]["Resource"][0] = 'arn:aws:s3:::' + bucket_name
        policy_name = bucket_name + '_' + bucket_set['permission'] + '_' + 'policy'
        policy_file_path = '../policy_json/' + policy_name + '.json'
        with open(policy_file_path, 'w') as f:
            json.dump(policy, f, ensure_ascii = False)
        # mc admin policy add aliasforost/ read_write_policys  ../policy_json/read_write_policy.json
        set_policy_response = set_policy(target = alias, policy_name = policy_name, policy_file_path = policy_file_path)
        if set_policy_response.content['status'] == 'success':
            logger.info("%s's policy is set successfully", bucket_name)
        elif set_policy_response.content['status'] == 'error':
            logger.error("%s's policy is set unsuccessfully", bucket_name)
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
    
    #set tags
    client.set_bucket_tags(bucket_name, tag_to_set)
    return True
  
def change_quota(**kwargs):
    if add_host:
        cmd = Command('mc {flags} admin bucket quota {target} --hard {quota}')
        return cmd(**kwargs)

def set_policy(**kwargs):
    if add_host:
        cmd = Command('mc {flags} admin policy add {target}/ {policy_name} {policy_file_path}')
        return cmd(**kwargs)


if __name__== "__main__" :
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
                logger.info('Finish creating %s and setting of %s successfully', bucket_name, bucket_name)
            else:
                logger.error('Errors occurs when creating %s or setting of %s', bucket_name, bucket_name)

    
    
    
               



    

    