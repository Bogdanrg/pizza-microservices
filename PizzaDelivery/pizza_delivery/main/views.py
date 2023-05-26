from django.contrib.auth import login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.db.models import Sum, Q, F

from .forms import *
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, FormView

from .models import Order
from .producer import send_data


def home(request):
    return render(request, template_name='main/home.html')


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'main/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registration"
        return context

    def form_valid(self, form):
        user = form.save()
        form.cleaned_data['property'] = 'created_user'
        login(self.request, user)
        send_data(form.cleaned_data)
        return redirect('home')


class UserLoginView(LoginView):
    template_name = 'main/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        return context


@method_decorator(decorator=login_required(login_url='login'), name='post')
class ChoicePizzaTypeView(ListView):
    template_name = 'main/order.html'
    context_object_name = 'types'

    def get_queryset(self):
        return PizzaType.objects.all().order_by('-price')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pizza type'
        return context

    def post(self, request, *args, **kwargs):
        order = Order.objects.safe_get(user=request.user.id)
        if not order:
            order = Order.objects.create(order_status='pending', user=request.user)
        pizza_type = PizzaType.objects.get(pizza_type_name=request.POST['pizza_type'])
        pizza = Pizza.objects.filter(Q(order=order.pk) & Q(pizza_type=pizza_type))
        if not pizza:
            Pizza.objects.create(pizza_type=pizza_type, quantity=request.POST['quantity'], order=order,
                                 pizza_size=request.POST['pizza_size'])
        else:
            pizza.update(quantity=F('quantity') + request.POST['quantity'])
        return redirect('ordering')


class ShoppingBasketView(LoginRequiredMixin, ListView):
    template_name = 'main/basket.html'
    login_url = 'login'
    context_object_name = 'pizzas'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Basket"
        query_set = self.get_queryset()
        if not query_set:
            return context
        total_sum = query_set.aggregate(total_sum=Sum(F("pizza_type__price") * F("quantity")))
        order = Order.objects.safe_get(user=self.request.user.id)
        order.total_price = total_sum['total_sum']
        order.save()
        context['total_sum'] = str(order.total_price)
        context['order_id'] = str(order.pk)
        context[self.context_object_name] = query_set
        return context

    def get_queryset(self):
        order = Order.objects.safe_get(user=self.request.user.id)
        if not order:
            return None
        return Pizza.objects.filter(order=order.pk).select_related('pizza_type')

    # def post(self, request, *args, **kwargs):
    # pizza = Pizza


def logout_user(request):
    logout(request)
    return redirect('home')
