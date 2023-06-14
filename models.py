from core.database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class PizzaType(Base):
    __tablename__ = 'pizza_type_table'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    pizza_type_name = Column(String(80), unique=True)
    description = Column(Text, nullable=True)


class Pizza(Base):
    __tablename__ = 'pizza_table'
    PIZZA_SIZES = (
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large'),
    )
    id = Column(Integer, primary_key=True)
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default='small')
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order_table.id'))
    order = relationship('Order', backref='pizzas')
    pizza_type_id = Column(Integer, ForeignKey('pizza_type_table.id'))
    pizza_type = relationship('PizzaType', backref='pizzas')


class Order(Base):
    __tablename__ = 'order_table'
    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    id = Column(Integer, primary_key=True)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default='PENDING')
    user_id = Column(Integer, ForeignKey('user_table.id'))
    user = relationship('User', backref='orders')

    def __repr__(self):
        return f"Order {self.id}"


class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    order = relationship('Order', backref='users')

    def __repr__(self):
        return f"User {self.username}"
