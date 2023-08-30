from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Item(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)
    photo = models.ImageField(upload_to='item_photos/', null=True, blank=True)
    is_retired = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.title} - {self.price}"



