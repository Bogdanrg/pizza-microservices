import time

from kafka import KafkaConsumer
from werkzeug.security import generate_password_hash
from services.order_service import get_order_by_id, get_pizza_type_by_name
from core.database import SessionLocal
from services.auth_service import get_user_by_username, get_user_by_email
from models import User, Order, Pizza
import json
from schemas import OrderModel


class MsgConsumer:
    def __init__(self, cfg: dict) -> None:
        self.consumer = KafkaConsumer(
            cfg['topic'],
            group_id=cfg['group_id'],
            bootstrap_servers=cfg['bootstrap_servers'],
            auto_offset_reset=cfg['auto_offset_reset'],
            enable_auto_commit=cfg['enable_auto_commit']
        )

    def start_consuming(self):
        for retrie in range(10):
            if self.consumer.bootstrap_connected():
                print("Consuming started")
                while True:
                    for message in self.consumer:
                        if json.loads(message.value).get('property') == 'created_user':
                            UserCRUD.create_user(json.loads(message.value))
                        elif json.loads(message.value).get('property') == 'created_order':
                            OrderCRUD.create_order(json.loads(message.value))
                        elif json.loads(message.value).get('property') == 'created_pizza':
                            OrderCRUD.create_pizza(json.loads(message.value))
            print("Connection refused")
            time.sleep(5)
        print("Max retries are spent")


class UserCRUD:
    """ CRUD methods for user"""

    @staticmethod
    def create_user(data: dict) -> None:
        db = SessionLocal()
        db_username = get_user_by_username(db, data.get('username'))
        if db_username is not None:
            raise ValueError("Data in microservices is different")
        db_email = get_user_by_email(db, data.get('email'))
        if db_email is not None:
            raise ValueError("Data in microservices is different")
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password1']),
            is_active=data.get('is_active', True),
            is_staff=data.get('is_staff', False)
        )
        db.add(new_user)
        db.commit()
        db.close()


class OrderCRUD:
    """ CRUD methods for orders"""

    @staticmethod
    def create_order(data: dict) -> None:
        db = SessionLocal()
        user = get_user_by_username(db, data.get('username'))
        new_order = Order(
            order_status=data.get('order_status'),
            user=user
        )
        db.add(new_order)
        db.commit()

    @staticmethod
    def create_pizza(data: dict):
        db = SessionLocal()
        order = get_order_by_id(db, data.get('order_id'))
        pizza_type = get_pizza_type_by_name(db, data.get('pizza_type'))
        new_pizza = Pizza(
            pizza_size=data.get('pizza_size'),
            quantity=data.get('quantity'),
            order=order,
            pizza_type=pizza_type
        )
        db.add(new_pizza)
        db.commit()

    @staticmethod
    def add_pizza_to_order(order: OrderModel, data: dict):
        pass


msg_consumer = MsgConsumer({
    "topic": "api_topic",
    "group_id": "api_group",
    "bootstrap_servers": "host.docker.internal:9090",
    "auto_offset_reset": 'earliest',
    "enable_auto_commit": True
})

msg_consumer.start_consuming()

print(msg_consumer.consumer.bootstrap_connected())
