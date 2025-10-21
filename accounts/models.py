from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# modified field of User model 
class User(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
