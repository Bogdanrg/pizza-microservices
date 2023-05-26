from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('ordering/', ChoicePizzaTypeView.as_view(), name='ordering'),
    path('shopping-basket', ShoppingBasketView.as_view(), name='basket'),
]
