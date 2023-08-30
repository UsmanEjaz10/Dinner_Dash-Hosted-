from django.db import models
from django.contrib.auth.models import User


# Create your models here. Consider it as table in DB
class Issue(models.Model):
    username = models.CharField(max_length= 50)
    phone = models.IntegerField()
    issue = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.username
 

