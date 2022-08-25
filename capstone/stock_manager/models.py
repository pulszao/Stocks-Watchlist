from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Transactions(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="transactions")
    operation = models.CharField(max_length = 3)
    symbol = models.CharField(max_length=10)
    shares = models.IntegerField()
    price = models.FloatField()
    date = models.DateTimeField()

class Watchlist(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
    listing_symbol = models.CharField(max_length=5)