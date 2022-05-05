# add_host.py

from bmc import config_host_add
from util import get_logger, endpoint, access_key, secret_key, alias

logger = get_logger('add_host')


def add_host():
    # new config host of minio
    url = "http://"+endpoint
    add_host = config_host_add(alias=alias, url=url,
                               username=access_key, password=secret_key)
    if add_host.content['status'] == 'success':
        logger.info('Add Host successfully')
        return True
    else:
        err_message = add_host.content['error']['message']
        err_cause = add_host.content['error']['cause']['message']
        logger.error('Add Host unsuccessfully')
        logger.error('Error Message: ' + err_message)
        logger.error('Error Cause: ' + err_cause)
        return False


if __name__ == "__main__":
    add_host()
