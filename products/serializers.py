from rest_framework.serializers import ModelSerializer
from .models import Category,Product

class CategorySerializer(ModelSerializer):
     class Meta:
          model = Category
          fields = ['id','name','description']

     def create(self, validated_data):
          category = Category.objects.create(
               name = validated_data['name'],
               description = validated_data['description']
          )
          return category     

class ProductSerializer(ModelSerializer):
     class Meta:
          model = Product
          fields = ['id','name','description','price','stock','category']

     def create(self, validated_data):
         product = Product.objects.create(
              name = validated_data['name'],
              description = validated_data['description'],
              price = validated_data['price'],
              stock = validated_data['stock'],
              category = validated_data['category']
         ) 
         return product    
