from  rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
     products = ProductSerializer(many=True, read_only=True)
     product_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), write_only=True
      )

     class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'product_ids', 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

     def create(self, validated_data):
        products = validated_data.pop('product_ids')
        user = self.context['request'].user
        total_price = sum(p.price for p in products)
        order = Order.objects.create(user=user, total_price=total_price)
        order.products.set(products)
        return order   
     
     def update(self, instance, validated_data):
        products = validated_data.pop('product_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if products is not None:
            instance.products.set(products)
            instance.total_price = sum(p.price for p in products)
        instance.save()
        return instance