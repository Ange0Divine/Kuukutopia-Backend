from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    F = "Female"
    M = "Male"
    O = "Other"
    ADMIN = "Admin"
    STOCK_MANAGER = "Stock-Manager"
    FARMER = "Farmer"
    CUSTOMER = "Customer"

    GENDER_CHOICES = [(F, "Female"), (M, "Male"), (O, "Other")]
    ROLE_CHOICES = [(ADMIN, "Admin"), (STOCK_MANAGER, "Stock-Manager"), (FARMER, "Farmer"), (CUSTOMER, "Customer")]
   
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=O)
    phone_number = models.CharField(max_length=15, unique=False)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
class StockManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Additional fields specific to stock managers can be added here

    def __str__(self):
        return f"Stock Manager: {self.user.username}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    
    # Additional fields specific to customers can be added here

    def __str__(self):
        return f"Customer: {self.user.username}"        
