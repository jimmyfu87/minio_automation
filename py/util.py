## util.py

from minio import Minio

# Single-Node
# endpoint = "127.0.0.1:9000/"
# access_key = "esun1313"
# secret_key = "esun1313"
# secure = False

# Distribute-Node
endpoint = "127.0.0.1:9000/"
access_key = "minio"
secret_key = "minio123"
secure = False


minio_client = Minio(
    endpoint = endpoint,
    access_key = access_key,
    secret_key = secret_key,
    secure = secure
)

# 使用者會給的Tag
required_tags = ['project_name', 'privacy_ind', 'purpose', 'permission']

# 若未指定預設的quota
optional_tags = {'quota' : "15"}

default_tags = {'usage' : '0', 'use_ratio' : '0', 'status' : 'Healthy'}


# minio_client = Minio(
#         "play.min.io",
#         access_key="Q3AM3UQ867SPQQA43P2F",
#         secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
# )