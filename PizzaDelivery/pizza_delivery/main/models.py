from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PizzaManager(models.Manager):
    def safe_get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Pizza.DoesNotExist:
            return None


class OrderManager(models.Manager):
    def safe_get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Order.DoesNotExist:
            return None


class PizzaType(models.Model):
    price = models.PositiveIntegerField(default=15)
    pizza_type_name = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to='pizza_photo')

    def __str__(self):
        return self.pizza_type_name


class Pizza(models.Model):
    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )
    pizza_size = models.CharField(max_length=250)
    pizza_type = models.ForeignKey("PizzaType", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="количество", default=1)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    objects = PizzaManager()

    def get_absolute_url(self):
        return reverse('basket-detail', kwargs={'pk': self.pk})


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'pending'),
        ('in-transit', 'in-transit'),
        ('delivered', 'delivered')
    )
    total_price = models.PositiveIntegerField(default=0)
    order_status = models.CharField(choices=ORDER_STATUS, default='pending', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = OrderManager()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['id']

    def __str__(self):
        return f"Order: {self.pk}, user: {self.user}"
