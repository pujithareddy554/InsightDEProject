import sys
import json
import csv
import boto3

# Reading the file with Boto3
# Get a handle on s3
s3 = boto3.resource('s3',aws_access_key_id='A******',aws_secret_access_key='****')
# Get a handle on the bucket that holds the file
response = s3.Object(bucket_name = 'myawsinsightbucket', key = "data/test-aws-insight.csv").get()
# Read the contents of the file and split it into a list of lines
lines = response['Body'].read().decode("utf-8-sig").split()
print(lines) # To check if file from S3 is read correctly

broker = str(sys.argv[1]) #"<EC2-instance-address>:9092"
topic = str(sys.argv[2])

def produce_kafka_stream(broker, topic):
    '''
    This method creats a Kafka stream on the topic given
    :param broker: A string indicating the Kafka broker server and the port on which the stream is running
    :param topic: A string indicating the Kafka topic on which the stream is going to be written
    '''

    # Produce a json data to send to Kafka topic
    producer = KafkaProducer(bootstrap_servers=[broker], value_serializer= lambda x: dumps(x).encode("utf-8"))
    print(lines,'in prod')
    for row in  csv.DictReader(lines, delimiter = ","):
        producer.send(topic, value = row)
        print(row)
    print("Data sent to Kafka topic:", topic)

if __name__ == "__main__":

    produce_kafka_stream(broker, topic)

