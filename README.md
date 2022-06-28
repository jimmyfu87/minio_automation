# minio_automation

## `create_apply.py`
### 用途：
- 使用json檔建立多個有tag的buckets
- 依據permission和quota設定policy和quota的limit，並建立user及綁定policy和user，也可用於單獨申請policy
### 使用方式：
    python create_apply.py -d {../json_data/init}

### 附註：
-d: 儲存所有json檔的資料夾路徑(`../json_data/init`)   
#### type   
- init
    - 代表project_name尚未建立為user，程式會先用project_name當作username建立user，會先檢查username是否存在
    - 若username已經存在，為避免覆蓋user，會中止後續所有動作
    - 若username不存在，則會建立user並繼續後續動作  
- extend
    - 代表project_name已經建立為user，程式會先檢查username是否存在
    - 若username未存在，會中止後續所有動作
    - 若username存在則繼續進行後續動作

            {
                "type" : "init",
                "project_name":"project1",
                "env": "Staging",
                "bucket":[
                    {
                        "bucket_name": "bucket1",
                        "quota": "20",
                        "privacy_ind": "Y",
                        "purpose": "model_used",
                        "save_type": "hard",
                        "management_unit":"A1",
                        "ttl": "30"
                    },
                    {
                        "bucket_name": "bucket2",
                        "quota": "30",
                        "privacy_ind": "N",
                        "purpose": "project_used",
                        "save_type": "hard",
                        "management_unit":"A1",
                        "ttl": "25"
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


## `buckets_summary.py`
### 用途： 
輸出所有buckets的object數量、所有tag的資料的dataframe的csv檔，並儲存至特定路徑  
### 使用方式： 
    python buckets_summary.py -f {file} -e {env}

### 附註：
-f: 輸出檔案的名稱{file}  
-e: 使用環境(env) 


## `projects_summary.py`
### 用途： 
輸出所有project所使用的buckets數量、objects數量、quota的總額的dataframe的csv檔，並儲存至特定路徑
### 使用方式： 
    python projects_summary.py -f {file} -e {env}

### 附註：
-f: 輸出檔案的名稱{file}   
-e: 使用環境(env) 


## `update_buckets_use.py`
### 用途： 
將所有buckets的usage, quota, use_ratio, status的tag按照使用的狀況進行更新
### 使用方式： 
    python update_buckets_use.py -e {env}

### 附註：
-e: 使用環境(env)


## add_host.py
### 用途： 
建立使用mc指令的alias，建立一次即可，create_buckets時，設定quota和policy時會使用到
### 使用方式： 
    python add_host.py -e {env}

### 附註：
-e: 使用環境(env)


## util.py
### 用途： 
儲存多個可客製化的參數，讓其餘程式可以重複利用，包含以下幾個部分 

(1) 設定buckets會有的tag種類
- required_tags(使用者必須給定的tag): 
        
            ['project_name', 'privacy_ind', 'purpose', 'quota', 'save_type', 'management_unit']
- default_tags(系統直接預設的Tag): 
            
            {'usage' : '0', 'use_ratio' : '0', 'status' : 'Healthy'}

(2) 當bucket的use_ratio大於value則給予key當作該buckets的status，若皆小於則視為healthy
- use_ratio_threshold_dic(bucket的status分類閥值的字典): 
            
            {'Danger': 80, 'Cautious': 40,  'Aware': 10}
- use_ratio_healthy_status_name(healthy狀態的名字): 
            
            'Healthy'

(3) policy
- policy的模板: read_only_policy(唯讀的policy, read_write_policy(讀寫的policy)
- 暫時存放policy產生json檔的路徑
#### Read Only policy template
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": [
                    "arn:aws:s3:::{{bucket_name}}/*"
                ]
            }
        ]
    }
#### Read Write policy template
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::{{bucket_name}}/*"
                ]
            }
        ]
    }


## `test.py`
### 用途： 
測試function的整合測試  

- 利用test_file/test_json建立兩個bucket，並進行測試
  - bucket是否建立成功、quota_limit是否設定正確、user是否設定正確
  - policy是否設定並綁定user、tag是否設定正確
 
- 放進1、10張圖片進入兩個bucket並進行update_bucket_use，並進行測試usage、use_ratio、status是否符合
 
- 輸出`projects_summary.csv`檔，並測試比對是否跟預期的csv檔(`test_folder/projects_summary.csv`)相同
 
- 輸出buckets_summary.csv檔，刪除create_date的欄位之後，並測試比對是否跟預期的csv檔(`test_folder/buckets_summary.csv`)相同
### 使用方式： 
    cd src
    python test.py -e {env}

### 附註：
-e: 使用環境(env)


## `export_minio.py`
### 用途： 
- 用於輸出minio的metadata，包括bucket、policy、user三個資料，需先建立以下路徑存放資料 
 
      export_data    
      export_data/policy    
一共會生成三種資料
- policy: 包括目前admin底下所有的policy資料的raw policy資料，檔名為該policy的名稱，範例如上面policy的template
- user_ls.json: 包含所有user的access key, 每個user被assign的policy，secret key無法取得會留空人工填寫，範例如下   
    
      [
        {
            "access_key": "project1",
            "secret_key": "",
            "policy_name": [
                "bucket1_RO_policy",
                "bucket2_RW_policy"
            ]
        },
        {
            "access_key": "project2",
            "secret_key": "",
            "policy_name": [
                "bucket3_RW_policy",
                "bucket4_RO_policy"
            ]
        }
      ]

- bucket_ls.json: 包含bucket的所有tag等資料

        [
            {
                "bucket_name": "bucket1",
                "project_name": "project1",
                "management_unit": "A1",
                "privacy_ind": "Y",
                "purpose": "model_used",
                "save_type": "hard",
                "quota": "20",
                "usage": "0",
                "use_ratio": "0",
                "status": "Healthy"
            },
            {
                "bucket_name": "bucket2",
                "project_name": "project1",
                "management_unit": "A1",
                "privacy_ind": "N",
                "purpose": "project_used",
                "save_type": "hard",
                "quota": "30",
                "usage": "0",
                "use_ratio": "0",
                "status": "Healthy"
            }
        ]

### 使用方式： 
    cd src
    python export_minio.py -e {env}

### 附註：
-e: 使用環境(env)

## `import_minio.py`
### 用途： 
用於輸入minio的metadata，從以下資料夾輸入包括bucket、policy、user的資料(需自行填寫secret key的資料後再輸入)，之後再使用mc mirror搬遷資料
 
      export_data    
      export_data/policy    


### 使用方式： 
    cd src
    python import_minio.py -e {env}

### 附註：
-e: 使用環境(env)

