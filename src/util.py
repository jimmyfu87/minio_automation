## util.py
from email import policy
import bmc
from minio import Minio

# Single-Node
# endpoint = "127.0.0.1:9000/"
# access_key = "esun1313"
# secret_key = "esun1313"
# secure = False

# Distribute-Node
endpoint = "127.0.0.1:9000"
access_key = "minio"
secret_key = "minio123"
secure = False
alias = 'aliasforost'


minio_client = Minio(
    endpoint = endpoint,
    access_key = access_key,
    secret_key = secret_key,
    secure = secure
)

### Tag
# 使用者會給的Tag
required_tags = ['project_name', 'privacy_ind', 'purpose', 'permission', 'quota']

# 系統直接預設的Tag
default_tags = {'usage' : '0', 'use_ratio' : '0', 'status' : 'Healthy'}

### project_columns


### Use ratio threshold
use_ratio_threshold_dic = {'Danger': 0.8, 'Cautious': 0.4,  'Aware': 0.1}
use_ratio_healthy_status_name = 'Healthy'

def add_host(): 
    # new config host of minio
    url = "http://" + endpoint
    add_host = bmc.config_host_add(alias = alias, url = url, username = access_key, password = secret_key)
    if add_host.content['status'] == 'success':
        print('Add Host successfully!')
        return True
    else:
        err_message = add_host.content['error']['message']
        err_cause = add_host.content['error']['cause']['message']
        print('Error Message: ' + err_message)
        print('Error Cause: ' + err_cause)
        return False

### Policy

read_only_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                 "arn:aws:s3:::bucket_name"
            ]
        }
    ]
}

read_write_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {   
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:DeleteObject"
            ],
            "Resource": [
                 "arn:aws:s3:::bucket_name"
            ]
        }
    ]
}

policy_set  = {'RO': read_only_policy, 'RW': read_write_policy}

# minio_client = Minio(
#         "play.min.io",
#         access_key="Q3AM3UQ867SPQQA43P2F",
#         secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
# )