## get_all_buckets.py

import util
import pandas as pd 
from dateutil import tz
import argparse

client = util.minio_client


def get_all_buckets_df():
    buckets = client.list_buckets();
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

def project_summary(df: pd.DataFrame):
    project_gp = df.groupby('project_name')

    # columns need to be count
    count_df = project_gp[['bucket_name']].count()
    count_df.rename(columns = {'bucket_name':'total_buckets'}, inplace = True)

    # columns need to be sum    
    sum_df = project_gp[['objects_num', 'quota' ]].sum()
    sum_df.rename(columns = {'objects_num':'total_objects','quota':'total_quota(GB)'}, inplace = True)

    # join two dataframe on index
    project_df = count_df.join(sum_df)

    return project_df


if __name__== "__main__" :
    # get filename by arg
    parser = argparse.ArgumentParser() 
    parser.add_argument("--filename", "-f", type=str, required=True, default = 'file')
    parser.add_argument("--purpose", "-p", type=str, required=True, default='ps')
    args = parser.parse_args()
    
    df = get_all_buckets_df()
    filename = args.filename + '.csv'
    purpose = args.purpose

    # ps means project_summary
    if  purpose == 'ps':
        project_df = project_summary(df)
        project_df.to_csv(filename)
    elif purpose == 'get_df':
        df.to_csv(filename)
    else:
        print('Unknown purpose')

    print('The file is saved successfully')