from django.db import models

# Create your models here.
class Products(models.Model):
    poultry = "Poultry"
    processed = "Processed"
    eggs = "Eggs"
    CATEGORY_CHOICES = [
        (poultry, "Poultry"),
        (processed, "Processed"),
        (eggs, "Eggs")
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    stock_Manager = models.ForeignKey('accounts.StockManager', on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.branch_name} - {self.location}"
    

class Inventory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.branch.branch_name} - {self.quantity}"
