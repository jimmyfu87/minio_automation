# buckets_summary.py

from util import minio_client as client
from util import get_logger, all_tags
import pandas as pd
from dateutil import tz
import argparse

logger = get_logger('buckets_summary')


def get_all_buckets_df():
    buckets = client.list_buckets()
    if len(buckets) == 0:
        logger.debug('There is no any buckets')
        empty_df = pd.DataFrame(columns=all_tags)
        return empty_df
    data = []
    for bucket in buckets:
        new_bucket = {}
        # set bucket_name
        new_bucket.update({'bucket_name': bucket.name})
        # set create_date
        local_zone = tz.tzlocal()
        local_date_time = bucket.creation_date.astimezone(local_zone)
        new_bucket.update({'create_time': local_date_time})
        # set the number of objects
        objects_num = len(list(client.list_objects(bucket.name,
                                                   recursive=True)))
        new_bucket.update({'objects_num': objects_num})
        # set tags
        new_bucket.update(client.get_bucket_tags(bucket.name))
        # append dic to list
        data.append(new_bucket)
    df = pd.DataFrame(data)
    df = df[['bucket_name', 'create_time', 'objects_num', 'privacy_ind',
             'project_name', 'purpose', 'quota',
             'usage', 'use_ratio', 'status']]
    # change numeric type column
    int_col = ['quota']
    float_col = ['usage', 'use_ratio']
    df['quota'] = df[int_col].astype('int')
    df['usage'] = df[float_col].astype('float')
    logger.info('The dataframe is created successfully')
    return df


if __name__ == "__main__":
    # get filename by arg
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", type=str,
                        required=False, default='buckets_summary')
    args = parser.parse_args()
    df = get_all_buckets_df()
    filename = args.filename + '.csv'
    try:
        df.to_csv(filename)
        logger.info('The file is saved successfully')
    except Exception:
        logger.error('The file is saved unsuccessfully')
