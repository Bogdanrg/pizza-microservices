from requests import get
from models import PizzaType
from core.database import SessionLocal


def get_pizza_types():
    response = get('http://django:8080/api/v1/pizza_types').json()
    db = SessionLocal()
    for pizza_type in response:
        new_pizza_type = PizzaType(
            price=pizza_type['price'],
            pizza_type_name=pizza_type['pizza_type_name'],
            description=pizza_type['description']
        )
        db.add(new_pizza_type)
    db.commit()
