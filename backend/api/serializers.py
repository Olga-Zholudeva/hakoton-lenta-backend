from rest_framework import serializers
from products.models import Sku


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар.'''
    class Meta:
        model = Sku
        fields = '__all__'
