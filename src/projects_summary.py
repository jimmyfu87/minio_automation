# projects_summary.py

import argparse
import pandas as pd
from buckets_summary import get_all_buckets_df
from util import get_logger

logger = get_logger('projects_summary')


def projects_summary(df: pd.DataFrame):
    project_gp = df.groupby('project_name')
    # columns need to be count
    count_df = project_gp[['bucket_name']].count()
    count_df.rename(columns={'bucket_name': 'total_buckets'}, inplace=True)
    # columns need to be sum
    sum_df = project_gp[['objects_num', 'quota']].sum()
    sum_df.rename(columns={'objects_num': 'total_objects',
                  'quota': 'total_quota(GB)'}, inplace=True)
    # join two dataframe on index
    project_df = count_df.join(sum_df)
    return project_df


if __name__ == "__main__":
    # get filename by arg
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", type=str,
                        required=False, default='projects_summary')
    args = parser.parse_args()
    df = get_all_buckets_df()
    filename = args.filename + '.csv'
    project_df = projects_summary(df)
    try:
        project_df.to_csv(filename)
        logger.info('The file is saved successfully')
    except Exception:
        logger.error('The file is saved unsuccessfully')
