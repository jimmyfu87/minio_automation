# minio_automation

## create_buckets.py
### 用途：
使用json檔建立多個有tag的buckets，會依據permission和quota設定policy和quota的limit
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


## add_host.py
### 用途： 
建立使用mc指令的alias，建立一次即可，create_buckets時，設定quota和policy時會使用到
### 使用方式： 
    python remove_all_buckets.py 


## util.py
### 用途： 
儲存多個可客製化的參數，讓其餘程式可以重複利用，包含以下幾個部分 

##### (1) 登入minio需要的值
###### endpoint, access_key, secret_key, secure, alias

##### (2) 設定buckets會有的tag種類
###### 1.required_tags(使用者必須給定的tag): ['project_name', 'privacy_ind', 'purpose', 'permission', 'quota']
###### 2.default_tags(系統直接預設的Tag): {'usage' : '0', 'use_ratio' : '0', 'status' : 'Healthy'}

##### (3) 當bucket的use_ratio大於value則給予key當作該buckets的status，若皆小於則視為healthy
###### 1. use_ratio_threshold_dic(bucket的status分類閥值的字典): {'Danger': 0.8, 'Cautious': 0.4,  'Aware': 0.1}
###### 2. use_ratio_healthy_status_name(healthy狀態的名字): 'Healthy'

##### (4) policy
###### 1. policy的模板: read_only_policy(唯讀的policy, read_write_policy(讀寫的policy)
###### 2. 暫時存放policy產生json檔的路徑: 

