from itertools import product
from random import choices
from django.db import models
from django.contrib.auth.models import User

class UpdateCreate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(UpdateCreate):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='b_products')
    stock = models.SmallIntegerField(blank=True, null=True)
    #! We used SmallIntegerField to take up less space in the database 👆

    def __str__(self):
        return self.name

class Firm(UpdateCreate):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Transaction(UpdateCreate):
    TRANSACTIONS = (
        ("1", "IN"),
        ("0", "OUT"),
    )
    #! When you say SET_NULL, it is necessary to write "null=True". When the user is deleted, that field in db will remain null 👇
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    firm = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True, related_name='transactions')
    #! SmallntegerField accepts numbers from -32768 to 32767 👇
    transaction = models.SmallIntegerField(choices=TRANSACTIONS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='transaction')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    #? 👆 Let's consider the price field to determine the product price for our model. Prices are in decimals. 10 lira is like 25 cents. "Float Field" and "Decimal Field" are the field types used for decimal numbers. The main difference of these is that Float Field accepts small numbers and "Decimal Field" accepts larger numbers. The maximum number of digits that Float Field can take is 7 and it occupies 4 bytes in the database. The maximum digit that Decimal Field can take is 29. It takes 16 bytes of space in the database. Another difference of Decimal Field is that the number of digits and the decimal part can be glazed. Decimal Field takes the max_digits and decimal_places arguments. max_digits is the maximum number of digits allowed. decimal_places is the number of decimal places to use. decimal_places cannot be greater than max_digits.
    def __str__(self):
        return f'{self.transaction} - {self.product} - {self.quantity}'