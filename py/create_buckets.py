## create_all_buckets.py

from util import minio_client, required_tags,  default_tags, optional_tags
from minio.commonconfig import Tags
import argparse
import json
import os

import logging


client = minio_client

json_data = {
    "bucket_name": "airflow-logs10",
    "project_name": "etl-teams",
    "privacy_ind": 'Y',
    "purpose": 'prject_used',
    "permission": 'RO',  
    "quota" : "10"
}

def create_buckets(bucket_set: dict ):
    # check bucket_name exists or not
    bucket_name = bucket_set['bucket_name']
    if client.bucket_exists(bucket_name):
        print('This bucket_name already exists')
    else:
        # make a bucket
        client.make_bucket(bucket_name)
        print(bucket_name, 'is created successfully')
        if set_bucket_tags(bucket_set):
            print(bucket_name, "s' tags are set successfully")
        else:
            print(bucket_name, "s' tags are set unsuccessfully")

def set_optional_tag(bucket_set: dict, tag_name: str, tag_to_set):
    if tag_name in bucket_set.keys():
        tag_to_set[tag_name] = bucket_set[tag_name]
    else:
        if tag_name in optional_tags.keys():
            tag_to_set[tag_name] = optional_tags[tag_name]
        else:
            print(tag_name, ' does not have input value or default value')



def set_bucket_tags(bucket_set: dict):
    bucket_name = bucket_set['bucket_name']
    tag_to_set = Tags.new_bucket_tags()
        
    # set required tags by json file
    for tag in required_tags:
        tag_to_set[tag] = bucket_set[tag]
    
    # set optional tags by json file
    for tag in optional_tags:
        set_optional_tag(bucket_set = bucket_set, tag_name = tag, tag_to_set = tag_to_set)
    
    # set default tags
    for key in default_tags.keys():
        tag_to_set[key] = default_tags[key]
    
    #set tags
    client.set_bucket_tags(bucket_name, tag_to_set)
    return True
  

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
            create_buckets(data)
               



    

    