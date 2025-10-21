from django.contrib import admin
from  .models import Product,Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ['id','name','description']

@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id','name', 'category', 'price', 'stock')
     list_filter = ('category',)
     search_fields = ('name',)