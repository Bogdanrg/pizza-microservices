from kafka import KafkaConsumer
from werkzeug.security import generate_password_hash

from core.database import SessionLocal
from services.auth_service import get_user_by_username, get_user_by_email
from models import User, Order
import json


consumer = KafkaConsumer(
    'api_topic',
    bootstrap_servers="host.docker.internal:9090",
)

while True:
    for message in consumer:
        data = json.loads(message.value)
        try:
            if data.get('property') == 'created_user':
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
            if data.get('property') == 'created_order':
                db = SessionLocal()
                user = get_user_by_username(db, data['user_name'])
                print(user, data)
                new_order = Order(
                    quantity=data['quantity'],
                    pizza_size=data['pizza_size'],
                    user=user
                )
                db.add(new_order)
                db.commit()
                db.close()
        except ValueError:
            print("Нет такого")
