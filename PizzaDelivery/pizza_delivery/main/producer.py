from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="kafka:29090"
)


def send_data(data):
    producer.send('api_topic', json.dumps(data).encode("utf-8"))
