from fastapi import FastAPI
from order_routes import order_router
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
from pizza_type_routes import pizza_type_router


app = FastAPI()


@AuthJWT.load_config
def set_config():
    return Settings()


app.include_router(order_router)
app.include_router(auth_router)
app.include_router(pizza_type_router)
