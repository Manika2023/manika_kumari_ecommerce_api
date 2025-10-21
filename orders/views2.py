from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from orders.models import  Order
from products.models import Product
from orders.serializers import OrderSerializer
from products.serializers import ProductSerializer
from .models import OrderItem
# Create your views here.

def home(request):
     return Response({"manika":"kumari"})

# api view for orders listing
class OrderListApi(APIView):
     permission_classes = [permissions.AllowAny]

     def get(self,request):
        try:  
          orders = Order.objects.all()
          serailizer = OrderSerializer(orders,many=True)
          return Response({
              "message":"Orders fetched successfully",
              "orders":serailizer.data
          },status=status.HTTP_200_OK)
        except:
          return Response({
              "message":"Orders are unable to fetched "
          },status=status.HTTP_400_BAD_REQUEST)

# api view for order detail    
class OrderDetailApi(APIView):
     permission_classes = [permissions.AllowAny]

     def get(self, request, pk):
        """Get details of specific order"""
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)
         


# api view for order create/add -> only by authenticated
class OrderCreateApi(APIView):
  permission_classes = [permissions.IsAuthenticated]
  def post(self, request):
    """
    Create a new order with quantities and decrease stock safely.
    """
    user = request.user
    products_input = request.data.get("products", [])

    if not products_input or not isinstance(products_input, list):
        return Response(
            {"message": "Products must be a non-empty list"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1️⃣ Aggregate quantities per product
    product_quantities = {}
    for item in products_input:
        product_id = item.get("id")
        quantity = item.get("quantity", 1)
        if not product_id or quantity <= 0:
            return Response(
                {"message": f"Invalid product entry: {item}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product_quantities[product_id] = product_quantities.get(product_id, 0) + quantity

    # 2️⃣ Validate products and calculate total
    total_price = 0
    valid_products = {}
    for product_id, quantity in product_quantities.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": f"Product with ID {product_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        valid_products[product] = quantity
        total_price += product.price * quantity

    # 3️⃣ Create order
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        status="pending"
    )

    # 4️⃣ Create OrderItems and decrease stock
    for product, quantity in valid_products.items():
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        try:
            product.decrease_stock(quantity)
        except ValueError:
            order.delete()  # rollback
            return Response(
                {"message": f"Insufficient stock for {product.name}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 5️⃣ Return serialized order
    serializer = OrderSerializer(order)
    return Response(
        {"message": "Order created successfully", "order": serializer.data},
        status=status.HTTP_201_CREATED
    )


# api view for update order
class OrderUpdateApi(APIView):
    permission_classes = [permissions.IsAuthenticated]     

    def post(self, request, pk):
        """
        Admin endpoint to update full order details:
        - products (via product_ids)
        - total_price (auto recalculated if products changed)
        - status
        """
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            updated_order = serializer.save()
            return Response({
                "message": "Order updated successfully",
                "order": OrderSerializer(updated_order).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDeleteApi(APIView):
    """delete order by admin"""    
    permission_classes = [permissions.IsAdminUser]

    def delete(self,request,pk):
        order = Order.objects.get(pk=pk,user=request.user)
        if not order:
            return Response({"message":"order not found"},status=status.HTTP_404_NOT_FOUND)
        order.delete()    
        return Response({
            "messsage":"order deleted successfully"
        })
    

# for notification
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer 