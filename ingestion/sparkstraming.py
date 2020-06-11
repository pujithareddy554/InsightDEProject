from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Chain-Track').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
streamPath = "s3a://myawsinsightbucket/data/"
topic = "testTopic"
broker = "localhost:9092"
# Subscribe the stream from Kafka
df_kafka = spark.readStream \
             .format("kafka") \
             .option("kafka.bootstrap.servers", broker) \
             .option("subscribe", topic) \
             .load()
df_kafka.printSchema()


