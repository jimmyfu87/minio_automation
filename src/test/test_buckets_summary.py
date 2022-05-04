# test_buckets_summary.py

import sys
sys.path.insert(0, '../')
from buckets_summary import get_all_buckets_df
import pandas as pd 

def test_get_all_buckets_df():
    assert type(get_all_buckets_df()) == pd.DataFrame
