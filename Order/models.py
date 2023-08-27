from django.db import models
from django.contrib.auth.models import User
from Item.models import Item


class Order(models.Model):
    STATUS_CHOICES = [
        ("ordered", "Ordered"),
        ("paid", "Paid"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="OrderItem")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Order {self.pk} ({self.user.username}) - {self.status}   {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item.title} x{self.quantity} in Order {self.order.pk}"
