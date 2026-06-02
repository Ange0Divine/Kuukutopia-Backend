from django.db import models

# Create your models here.
class Payment(models.Model):
    pending = "Pending"
    completed = "Completed"
    failed = "Failed"

    STATUS_CHOICES = [
        (pending, "Pending"),
        (completed, "Completed"),
        (failed, "Failed")
    ]
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"