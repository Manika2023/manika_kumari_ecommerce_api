from django.urls import path
from .views import AddToCartView, PlaceOrderView, UpdateOrderStatusView

urlpatterns = [
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('order/place/', PlaceOrderView.as_view(), name='place_order'),
    path('order/update/<int:order_id>/<str:new_status>/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]

