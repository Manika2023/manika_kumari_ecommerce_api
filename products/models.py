from django.db import models

#  Category model
class Category(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100, unique=True) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    # better than IntegerField for money
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    # stock should not be negative
    stock = models.PositiveIntegerField(default=0) 
    category = models.ForeignKey(
        Category,
        # delete products if category is deleted
        on_delete=models.CASCADE,    
        # allows category.products.all()
        related_name='products'     
    )

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def decrease_stock(self, quantity=1):
        """Helper method to reduce stock when ordered."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            print(f"Stock for {self.name} decreased by {quantity}. New stock: {self.stock}")
            print("stock is: ",self.stock)

        else:
            raise ValueError("Insufficient stock available")