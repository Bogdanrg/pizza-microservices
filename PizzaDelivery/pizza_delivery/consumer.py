import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza_delivery.settings")
django.setup()
from kafka import KafkaConsumer
from main.models import Order, User
import json


consumer = KafkaConsumer(
    "admin",
    bootstrap_servers="host.docker.internal:9990"
)
print("queue listening: ")

while True:
    for message in consumer:
        print("received")
        consumed_message = json.loads(message.value)
        try:
            if consumed_message['property'] == 'created_user':
                del consumed_message['property']
                User.objects.create_user(**consumed_message)
                print("User created")
            elif consumed_message['property'] == 'created_order':
                del consumed_message['property']
                Order.objects.create(**consumed_message)
                print("Order has created")
        except TypeError:
            print("Wrong type")
