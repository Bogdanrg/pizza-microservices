from models import Order, PizzaType
from sqlalchemy.orm import Session
from schemas import PizzaTypeModel


def get_order_by_id(db: Session, id: int):
    order = db.query(Order).filter(Order.id == id).first()
    return order


def get_pizza_type_by_name(db: Session, name: str) -> PizzaTypeModel:
    return db.query(PizzaType).filter(PizzaType.pizza_type_name == name).first()
