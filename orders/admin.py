from django.contrib import admin
from .models import Order,OrderItem,Cart,CartItem
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','product','order']

@admin.register(Cart)    
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    
@admin.register(CartItem)    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','quantity']