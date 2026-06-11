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

    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    REJECTED = "Rejected"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (REJECTED, "Rejected"),
    ]

    KG = "kg"
    PCS = "pcs"
    DOZEN = "dozen"
    TRAYS = "trays"
    LITRES = "litres"
    UNIT_CHOICES = [
        (KG, "kg"),
        (PCS, "pcs"),
        (DOZEN, "dozen"),
        (TRAYS, "trays"),
        (LITRES, "litres"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=PCS)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.branch.branch_name} - {self.quantity}"
