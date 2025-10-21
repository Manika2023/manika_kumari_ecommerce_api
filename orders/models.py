from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.conf import settings

# Create your models here.

class Order(models.Model):
     id = models.AutoField(primary_key=True)  #  explicitly define the ID
     STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     products = models.ManyToManyField(Product ,through='OrderItem')  # using through table
     total_price = models.DecimalField(max_digits=15,decimal_places=2)
     status = models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=10)
     updated_at = models.DateTimeField(auto_now_add=True)
     created_at = models.DateTimeField(auto_now=True)


     def __str__(self):
        return f"Order #{self.id} ({self.status})"

# Intermediate model - keeps track of quantity for each product in cart
# Through table to store quantity per product
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # quantity of this product

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order of order id #{self.order.id}"
    

# Cart model - holds products added by a user before placing an order
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'s Cart"


# Intermediate model - keeps track of quantity for each product in cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)    