# test_projects_summary.py
import sys
sys.path.insert(0, '../')
from projects_summary import projects_summary
from util import HOME_PATH
import pandas as pd
from os.path import join


def test_projects_summary():
    bucket_path = join(HOME_PATH,
                       'src/test/test_file/test_buckets_summary.csv')
    project_path = join(HOME_PATH,
                        'src/test/test_file/test_projects_summary.csv')
    buckets_summary_df = pd.read_csv(bucket_path)
    projects_summary_df = pd.read_csv(project_path)
    projects_summary_df.set_index('project_name', inplace=True)
    new_projects_summary_df = projects_summary(buckets_summary_df)
    assert new_projects_summary_df.equals(projects_summary_df)
