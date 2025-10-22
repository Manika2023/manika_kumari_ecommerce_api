from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Cart, CartItem, Order
from products.models import Product

# class view for as to cart
@method_decorator(csrf_exempt, name='dispatch')  
class AddToCartView(APIView):
    # user must be logged in
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request, product_id):
        """
        Add a product to the authenticated user's cart.
        If the product already exists, increase quantity.
        """
        product = get_object_or_404(Product, id=product_id)

        # Get or create the user's cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Add or update the product in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response(
            {"message": "Product added to cart."},
            status=status.HTTP_200_OK
        )

# class view for place an order
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Create an order from the user's cart.
        Clears the cart after placing the order.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            order.products.add(item.product)

        # Clear cart
        cart_items.delete()

        return Response(
            {"message": "Order placed successfully.", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )

# class view for update the status of products
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, order_id, new_status):
        """
        Update an order's status and notify user via WebSocket.
        """
        order = get_object_or_404(Order, id=order_id)

        # Update the order status
        order.status = new_status
        order.save()

        # --- WebSocket notification to frontend via Django Channels ---
        channel_layer = get_channel_layer()
        print("channel layer",channel_layer)
        async_to_sync(channel_layer.group_send)(
            "testingadmin_user_group",
            {
                "type": "order_status",
                "order_id": order.id,
                "status": order.status,
               "total_price": int(order.total_price),  
               "products": [
                    {"Product_id": p.id, "name": p.name, "price": int(p.price)}
                    for p in order.products.all()
]
            }
        )
        # ----------------------------------------------------------------

        return Response(
            {"message": f"Order status updated to {new_status}."},
            status=status.HTTP_200_OK
        )
