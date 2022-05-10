# minio_automation

## create_apply.py
### 用途：
使用json檔建立多個有tag的buckets，會依據permission和quota設定policy和quota的limit，並建立user及綁定policy和user，也可用於單獨申請policy
### 使用方式：
    python create_apply.py -d {../json_data/init}

### 附註：
-d: 儲存所有json檔的資料夾路徑(../json_data/init)   
#### type   
1.init: 代表project_name尚未建立為user，程式會先用project_name當作username建立user，會先檢查username是否存在，若username已經存在，為避免覆蓋user，會中止後續所有動作，若不存在，則會建立user並繼續後續動作  
2.extend: 代表project_name已經建立為user，程式會先檢查username是否存在，若username未存在，會中止後續所有動作，若username存在則繼續進行後續動作

    {
        "type" : "init",
        "project_name":"project1",
        "bucket":[
            {
                "bucket_name": "bucket1",
                "quota": "20",
                "privacy_ind": "Y",
                "purpose": "model_used"
            },
            {
                "bucket_name": "bucket2",
                "quota": "30",
                "privacy_ind": "N",
                "purpose": "project_used"
            }
        ],
        "policy": [
            {
                "bucket_name": "bucket1",
                "permission": "RO"
            },
            {
                "bucket_name": "bucket2",
                "permission": "RW"
            }
        ]
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


## add_host.py
### 用途： 
建立使用mc指令的alias，建立一次即可，create_buckets時，設定quota和policy時會使用到
### 使用方式： 
    python add_host.py 


## util.py
### 用途： 
儲存多個可客製化的參數，讓其餘程式可以重複利用，包含以下幾個部分 

##### (1) 登入minio需要的值
###### endpoint, access_key, secret_key, secure, alias

##### (2) 設定buckets會有的tag種類
###### 1.required_tags(使用者必須給定的tag): ['project_name', 'privacy_ind', 'purpose', 'quota']
###### 2.default_tags(系統直接預設的Tag): {'usage' : '0', 'use_ratio' : '0', 'status' : 'Healthy'}

##### (3) 當bucket的use_ratio大於value則給予key當作該buckets的status，若皆小於則視為healthy
###### 1. use_ratio_threshold_dic(bucket的status分類閥值的字典): {'Danger': 0.8, 'Cautious': 0.4,  'Aware': 0.1}
###### 2. use_ratio_healthy_status_name(healthy狀態的名字): 'Healthy'

##### (4) policy
###### 1. policy的模板: read_only_policy(唯讀的policy, read_write_policy(讀寫的policy)
###### 2. 暫時存放policy產生json檔的路徑: 

## test.py
### 用途： 
測試function的整合測試 
##### (1) 利用test_file/test_json建立兩個bucket，並進行測試bucket是否建立成功、quota_limit是否設定正確、user是否設定正確、policy是否設定並綁定user、tag是否設定正確
##### (2) 放進1、10張圖片進入兩個bucket並進行update_bucket_use，並進行測試usage、use_ratio、status是否符合
##### (3) 輸出projects_summary.csv檔，並測試比對是否跟預期的csv檔(test_folder/projects_summary.csv)相同
##### (3) 輸出buckets_summary.csv檔，刪除create_date的欄位之後，並測試比對是否跟預期的csv檔(test_folder/buckets_summary.csv)相同
### 使用方式： 
    cd src
    python test.py

