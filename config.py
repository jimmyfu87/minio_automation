#  mc event add Staging/bucket1 arn:minio:sqs::primary:mysql --event s3:ObjectCreated:Put
#  mc admin config set Staging notify_mysql:primary enable="off" format="namespace" dsn_string="root:example@tcp(localhost:3306)/db"  table="minio_images" queue_dir="" queue_limit="0" max_open_connections="2" 
#  mc admin config set Staging notify_kafka enable="off" topic="bucketevent" brokers="localhost:9902" sasl_username="" sasl_password="" sasl_mechanism="plain" client_tls_cert="" client_tls_key="" tls_client_auth=0 sasl="off" tls="off" tls_skip_verify="off" queue_limit=0 queue_dir="" version="" 
#  mc event add  Staging/im arn:minio:sqs::1:kafka --suffix .jpg
#  mc event add Staging/images arn:minio:sqs::primary:mysql --suffix .jpg
#  mc event add Staging/images arn:minio:sqs::1:mysql

#  mc admin config set Staging notify_mysql:primary enable="off" format="namespace" dsn_string="root:example@tcp(docker.for.mac.localhost:3306)/db"  table="minio_images" queue_dir="" queue_limit="0" max_open_connections="2" 

#  mc event add Staging/images arn:minio:sqs::1:postgresql --suffix .jpg

#  mc admin config set Staging notify_postgres connection_string="host=docker.for.mac.localhost port=5432 username=root password=example database=minio  sslmode=disable"
#  mc event add Staging/images arn:minio:sqs::_:postgresql --suffix .jpg


#  notify_postgres format=namespace connection_string="host=docker.for.mac.localhost dbname=db user=root password=example port=5432 sslmode=disable" table=min queue_dir= queue_limit=0 max_open_connections=2
#  mc admin config reset Staging/ notify_kafka 