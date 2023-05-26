from kafka import KafkaProducer
import json


producer = KafkaProducer(bootstrap_servers="kafka-1:29090")


def send_data(data):
    print(data)
    producer.send('admin', json.dumps(data).encode('utf-8'))
