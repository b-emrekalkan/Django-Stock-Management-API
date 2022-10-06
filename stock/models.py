from tkinter import CASCADE
from django.db import models

class UpdateCreate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=25)

class Brand(models.Model):
    name = models.CharField(max_length=30)

class Product(UpdateCreate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=CASCADE, related_name='products')

