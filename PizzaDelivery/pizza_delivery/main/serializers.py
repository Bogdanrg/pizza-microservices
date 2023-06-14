from rest_framework import serializers
from .models import PizzaType


class PizzaTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for pizza types
    """

    class Meta:
        model = PizzaType
        exclude = ('id', 'photo')
