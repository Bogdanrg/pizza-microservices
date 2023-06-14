from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from services.model_service import get_pizza_types

pizza_type_router = APIRouter(
    prefix='/service',
    tags=['service']
)


@pizza_type_router.get('/update_pizzas')
def update_pizza_types():
    get_pizza_types()
    return jsonable_encoder("updated")
