from django.db import models

# Create your models here.
class Order(models.Model):
    pending = "Pending"
    completed = "Completed"
    cancelled = "Cancelled"

    STATUS_CHOICES = [
        (pending, "Pending"),
        (completed, "Completed"),
        (cancelled, "Cancelled")
    ]
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} for {self.customer.user.username}"
    
class Sales(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Products', on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Sale of {self.product.name} to {self.user.username}"
    
class CartItem(models.Model):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.customer.user.username}"    