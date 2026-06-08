from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

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

    def __str__(self):
        return f"Stock Manager: {self.user.username}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.user.username}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    @staticmethod
    def generate_token():
        return str(random.randint(10000, 99999))

    def __str__(self):
        return f"Reset token for {self.user.username}"
