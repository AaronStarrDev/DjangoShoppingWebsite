from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0.00)

