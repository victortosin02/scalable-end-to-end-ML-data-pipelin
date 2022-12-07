import logging as log
import time
from threading import Thread
from pyspark.sql import *
from pyspark.ml.feature import VectorAssembler
import subprocess
from pyspark.ml.regression import LinearRegression
import time


class MLModelTrainerThread(Thread):
    __instance = None

    def __init__(self, thread_status=False):
        """ Constructor"""
        Thread.__init__(self)
        self.is_thread_alive = thread_status
        self.spark_session = None
        self.test_df = None

        if MLModelTrainerThread.__instance is None:
            MLModelTrainerThread.__instance = self
        else:
            log.error("cannot create another instance: ML Model Trainer")
            raise Exception("You cannot create another Machine Learning model trainer")

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MLModelTrainerThread.__instance is None:
            MLModelTrainerThread()
        return MLModelTrainerThread.__instance

    def run(self):
        print("START: Model Trainer Thread")
        self.create_spark_session()
        while self.is_thread_alive:
            self.is_thread_alive = False
            if self.is_file_exists():
                spark = self.spark_session
                df = spark.read.csv("hdfs://ip-172-31-0-181.ec2.internal:8020/dataset/boston.csv", inferSchema=True,
                                header=True)
                splits = self.test_train_split(df)
                train_df = splits[0]
                self.test_df = splits[1]
                lr = LinearRegression(featuresCol='features', labelCol='medv', maxIter=10, regParam=0.3, elasticNetParam=0.8)
                lr_model = lr.fit(train_df)
                lr_model.save("/home/hadoop/model")
                if self.is_mv_dataset_within_hdfs_success("/dataset/boston.csv", "/dataset/trained/"+"boston"+str(int(time.time()))+".csv"):
                    print("Model Training Complete")
            time.sleep(10)
            self.is_thread_alive = True

    def test_train_split(df):
        vector_assembler = VectorAssembler(
            inputCols=['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'black',
                       'lstat'], outputCol='features')
        df_tf = vector_assembler.transform(df)
        df_tf = df_tf.select(['features', 'medv'])

        return df_tf.randomSplit([0.7, 0.3])

    def create_spark_session(self):
        self.spark_session = SparkSession.builder.getOrCreate()

    def is_file_exists(self):
        proc = subprocess.Popen(['hadoop', 'fs', '-test', '-e', '/dataset/boston.csv'])
        proc.communicate()
        if proc.returncode == 0:
            return True
        else:
            return False

    def is_mv_dataset_within_hdfs_success(self, src_path, dst_path):
        proc = subprocess.Popen(["hdfs", "fs", "-mv", "-f", src_path, dst_path])
        proc.communicate()
        if proc.returncode == 0:
            return True
        else:
            return False
