# util.py
import logging
from minio import Minio
from jinja2 import Template

HOME_PATH = '/Users/jimmyfu87/Github/esun/minio_automation'


def get_logger(name):
    logging.basicConfig(format='%(asctime)s [%(levelname)s]'
                        + '%(name)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


# Distribute-Node
endpoint = "127.0.0.1:9000"
access_key = "minio"
secret_key = "minio123"
secure = False
alias = 'aliasforost'


minio_client = Minio(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=secure
)

# Tag
# 使用者會給的Tag
required_tags = ['project_name', 'privacy_ind', 'purpose',
                 'quota']

# 系統直接預設的Tag
default_tags = {'usage': '0', 'use_ratio': '0', 'status': 'Healthy'}

# 所有的Tag
all_tags = required_tags + list(default_tags.keys())

# Use ratio threshold
use_ratio_threshold_dic = {'Danger': 0.8, 'Cautious': 0.4,  'Aware': 0.1}
use_ratio_healthy_status_name = 'Healthy'

# the length of password
password_len = 8

# Policy
policy_directory = 'policy_json'
read_only_policy = \
                    '''{
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
                                    "arn:aws:s3:::{{bucket_name}}/*"
                                ]
                            }
                        ]
                    }'''

read_write_policy = \
                    '''{
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
                                    "arn:aws:s3:::{{bucket_name}}/*"
                                ]
                            }
                        ]
                    }'''


policy_temp_set = {'RO': Template(read_only_policy),
                   'RW': Template(read_write_policy)}
