## get_all_buckets.py

from util import minio_client as client
import pandas as pd 
from dateutil import tz
import argparse


def get_all_buckets_df():
    buckets = client.list_buckets();
    if len(buckets) == 0:
        print('There is no any buckets')
        raise 
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
        objects_num = len(list(client.list_objects(bucket.name)))
        new_bucket.update({'objects_num': objects_num})
        
        # set create_date
        new_bucket.update(client.get_bucket_tags(bucket.name))
        
        # append dic to list
        data.append(new_bucket)
    
    df = pd.DataFrame(data)

    # change numeric type column
    int_col = ['quota']
    float_col = ['usage', 'use_ratio']
    df['quota'] = df[int_col].astype('int')
    df['usage'] = df[float_col].astype('float')
    
    print('The dataframe is created successfully')
    return df


if __name__== "__main__" :
    # get filename by arg
    parser = argparse.ArgumentParser() 
    parser.add_argument("--filename", "-f", type = str, required = False, default = 'buckets_summary')
    args = parser.parse_args()
    
    df = get_all_buckets_df()
    filename = args.filename + '.csv'
    df.to_csv(filename)

    print('The file is saved successfully')