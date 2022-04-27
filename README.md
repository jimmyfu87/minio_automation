# minio_automation

## create_buckets.py
### 用途：
使用json檔建立多個有tag的buckets
### 使用方式：
    python create_buckets.py -dir {../json_data}

### 附註：
-dir: 儲存所有json檔的資料夾路徑(../json_data)

取得json_data資料夾的所有json檔，建立多個有tag的buckets，json檔範例如下  
    
    {
        "bucket_name": "bucket1",
        "project_name": "project1",
        "privacy_ind": "Y",
        "purpose": "project_used",
        "permission": "RO",  
        "quota" : "20"
    }  


## buckets_summary.py
### 用途： 
輸出所有buckets的object數量、所有tag的資料的dataframe的csv檔，並儲存至特定路徑  
### 使用方式： 
    python buckets_summary.py -f {file} 

### 附註：
-f: 輸出檔案的名稱{file}  


## projects_summary.py
### 用途： 
輸出所有project所使用的buckets數量、objects數量、quota的總額的dataframe的csv檔，並儲存至特定路徑
### 使用方式： 
    python projects_summary.py -f {file} 

### 附註：
-f: 輸出檔案的名稱{file}  


## update_buckets_use.py
### 用途： 
將所有buckets的usage, quota, use_ratio, status的tag按照使用的狀況進行更新
### 使用方式： 
    python update_buckets_use.py 


## remove_all_buckets.py
### 用途： 
刪除所有的buckets(所有buckets需均為空)
### 使用方式： 
    python remove_all_buckets.py 



