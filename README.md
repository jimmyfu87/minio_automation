# minio_automation

#### create_buckets.py
用途： 使用json檔建立多個有tag的buckets
使用方式： python create_buckets.py -dir {../json_data}

附註：
(參數1 -dir): 儲存所有json檔的資料夾路徑(../json_data)

取得json_data資料夾的所有json檔，建立多個有tag的buckets，json檔範例如下
{
    "bucket_name": "bucket1",
    "project_name": "project1",
    "privacy_ind": "Y",
    "purpose": "project_used",
    "permission": "RO",  
    "quota" : "0"
}

#### get_all_buckets.py
用途： 
(1) 輸出所有buckets的object數量、所有tag的資料的dataframe的csv檔，並儲存至特定路徑
(2) 輸出所有project所使用的buckets數量、objects數量、quota的總額的dataframe的csv檔，並儲存至特定路徑
使用方式： python get_all_buckets.py -f {file} -p {ps}

附註：
(參數1 -f): 輸出檔案的名稱{file}
(參數2 -p): 輸出檔案的用途{ps}

get_df: 用途(1)，輸出可參考sample_output/df.csv
ps : 用途(2)，輸出可參考sample_output/project_summary.csv


#### remove_all_buckets.py
用途： 刪除所有的buckets
使用方式： python remove_all_buckets.py 



