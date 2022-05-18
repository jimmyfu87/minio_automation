# add_host.py

from bmc import config_host_add
import json
import argparse
from util import get_logger, env_file_dir

logger = get_logger('add_host')


def add_host(env_name):
    env_filename = env_file_dir + '/' + env_name + '.json'
    # open environment json file and add host
    with open(env_filename) as env_json:
        env_data = json.load(env_json)
        alias = env_data['alias']
        endpoint = env_data['endpoint']
        access_key = env_data['access_key']
        secret_key = env_data['secret_key']
    # new config host of minio
    url = "http://" + endpoint
    add_host = config_host_add(alias=alias, url=url,
                               username=access_key, password=secret_key)
    if add_host.content['status'] == 'success':
        logger.info('Add %s Host successfully', env_name)
        return True
    else:
        err_message = add_host.content['error']['message']
        err_cause = add_host.content['error']['cause']['message']
        logger.error('Add %s Host unsuccessfully', env_name)
        logger.error('Error Message: ' + err_message)
        logger.error('Error Cause: ' + err_cause)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # get directory of json data by arg
    parser.add_argument("--env", "-e", type=str, required=True)
    args = parser.parse_args()
    add_host(args.env)
