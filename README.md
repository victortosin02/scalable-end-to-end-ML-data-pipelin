# Scalable-end-to-end-ML-data-pipeline using Kafka Streaming
![ML-work-flow](assets/pipeline_architecture.png?raw=true)
    
Automated the Machine Learning workflow by creating a continuous dataflow into ML model using Kafka streams that can then be
used for prediction. The training dataset is there in Hadoop filesystem and then using batch processing the data is processed and the
model is trained using spark.


Here are the steps before running the application:

+ I ran the shell script setup.sh. This installed all the required library dependencies.

+ Get fs.defaultFS property from /etc/hadoop/conf/core-site.xml.

+ Add the fs.defaultFS property string to HDFS_DATASET_LOC = "hdfs://ip-172-31-0-181.ec2.internal:8020/dataset/boston.csv" parameter in GlobalConstants.py.

+ SCP the boston.csv to HDFS. create a folder called "dataset" inside hdfs root. Create one more folder inside "dataset" folder called "used_dataset"

+ Put the boston.csv file inside "Dataset" folder in Source code to HDFS /dataset directory.

+ Downloaded the latest binary Kafka release from https://kafka.apache.org/downloads to my local machine and SCP to aws emr master node /home/hadoop

+ Unzip the kafka package using "tar -xzf kafka_2.13-3.3.1.tgz"

+ Ran the following commands in the terminal:
```console
cd kafka_2.13-3.3.1
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
```
    
+ SSH to emr master node from one more terminal. get into kafka_2.13-3.3.1 folder and run the following command
```console
./bin/kafka-topics.sh --create --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092 --topic sample
```
+ Now start the application by executing the shellscript run.sh
