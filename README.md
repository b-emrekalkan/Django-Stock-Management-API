# <center> 🛒 DJANGO-STOCK-MANAGAMENT-API 🛒 </center>

## <center> ************************************** </center>

# <center> 🚀 INITIAL SETUP </center>

```bash
# CREATING VIRTUAL ENVIRONMENT
# windows 👇
python -m venv env
# linux / Mac OS 👇
vitualenv env

# ACTIVATING ENVIRONMENT
# windows 👇
source env/Scripts/activate
# linux / Mac OS 👇
source env/bin/activate

# PACKAGE INSTALLATION
# if pip does not work try pip3 in linux/Mac OS
pip install djangorestframework
pip freeze > requirements.txt
django-admin startproject main .
# alternatively python -m pip install django
pip install python-decouple
django-admin --version
```

```bash
# 💨 If you already have a requirement.txt file, you can install the packages in the file
# 💨 by entering the following commands respectively in the terminal 👇
1-python -m venv env
2-source env/Scripts/activate
3-pip install -r requirements.txt 🚀
4-python.exe -m pip install --upgrade pip
5-python manage.py migrate
6-python manage.py createsuperuser
7-python manage.py runserver
```

## 🛑 Secure your project

## 🚩 .gitignore

✔ Add a ".gitignore" file at same level as env folder, and check that it includes ".env" and /env lines.

🔹 Do that before adding your files to staging area, else you will need extra work to unstage files to be able to ignore them.

🔹 [On this page](https://www.toptal.com/developers/gitignore) you can create "gitignore files" for your projects.

## 🚩 Python Decouple

💻 To use python decouple in this project, first install it 👇

```bash
pip install python-decouple
```

💻 Go to terminal to update "requirements.txt"  👇

```bash
pip freeze > requirements.txt
```

✔ Create a new file and name as ".env" at same level as env folder

✔ Copy your SECRET_KEY from settings.py into this .env file. Don't forget to remove quotation marks and blanks from SECRET_KEY

```python
SECRET_KEY=-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j
```

✔ Go to "settings.py", make amendments below 👇

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

## 💻 INSTALLING DJANGO REST

💻 Go to terminal 👇

```bash
python manage.py makemigrations
python manage.py migrate
pip install djangorestframework
```

✔ Go to "settings.py" and add 'rest_framework' app to INSTALLED_APPS

## 💻 PostgreSQL Setup

💻 To get Python working with Postgres, you will need to install the “psycopg2” module👇

```bash
pip install psycopg2
```

💻 Go to terminal to update requirements.txt  👇

```bash
pip freeze > requirements.txt
```

✔ Go to settings.py and add '' app to INSTALLED_APPS

## 💻 MIGRATE 👇

```bash
python manage.py migrate
```

## 🚀 RUNSERVER 👇

```bash
python manage.py runserver
```

# <center> ✏ This is the end of initial setup ✏ </center>

## <center> ****************************************************** </center>

# <center> 🚀 AUTHENTICATION </center>

## 🚩 ADDING AN APP

💻 Go to terminal 👇

```bash
python manage.py startapp account
```

✔ Go to "settings.py" and add 'account' app to "INSTALLED_APPS"

## 💻 INSTALL [DJ-REST-AUTH](https://dj-rest-auth.readthedocs.io/en/latest/)

```bash
pip install dj-rest-auth
```

💻 Go to terminal to update "requirements.txt"  👇

```bash
pip freeze > requirements.txt
```

## 🚩 Add "dj_rest_auth" app to "INSTALLED_APPS" in your django "settings.py" 👇

```python
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
```

## 🚩 Go to "main/urls.py" and add the path 👇

```python
path('users/', include('users.urls'))
```

## ✔ Create "urls.py" file under "users" App 👇
## 🚩 Go to "users/urls.py" and add 👇
```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
]
```

## 💻 Migrate your database
```bash
python manage.py migrate
```

## ✔ Create "serializers.py" file under "users" App and add 👇
```python
from rest_framework import serializers, validators
# from django.contrib.auth.models import User
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}

    )

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password1'
        )

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                {"password": "Password didn't match..... "}
            )
        return data

    #! To create a user when the user is registered 👇
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop('password1')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

```
## 🚩 Go to "views.py"
```python
from operator import ge
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
```

## 🚩 Go to "urls.py" and add the path 👇
```python
path('register/', RegisterView.as_view()),
```

## 🚩 Go to "base.py" and add 👇
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

## 🚩 Create "signals.py" under "user" App and add 👇
```python
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

## 🚩 Go to "apps.py" and add this under UsersConfig() 👇
```python
def ready(self) -> None:
    import users.signals
```

## 🚩 Go to "views.py" and customize RegisterView()👇
```python
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    #! When user register 👉 "username", "email","first_name","last_name" and "token" will be returned. 👇
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User does not have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

## 🚩 Override TokenSerializer() 👇
```python
from dj_rest_auth.serializers import TokenSerializer

#! We need to override the TokenSerializer to return all user data in a single request.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {
            'username',
            'email'
        }

class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = {
            'key',
            'user'
        }
```

## 🚩 Go to "base.py" and add 👇
```python
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.CustomTokenSerializer',
}
```
## <center> ****************************************************** </center>

## 🚩 ADDING APP

💻 Go to terminal 👇

```bash
python manage.py startapp stock
```

✔ Go to "settings.py" and add 'stock' app to "INSTALLED_APPS"

## 🚩 Go to "main.urls.py" and add path 👇

```python
 path('stock/', include('stock.urls')),
```

## 🚩 Go to "model.py" under "stock" app and create models 👇

```python
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
```

## 💻 Migrate your database

```bash
python manage.py migrate
```

## 🚩 Go to admin.py and register the models 👇

```python
from django.contrib import admin

from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Firm)
admin.site.register(Transaction)
```

## 🚩 Create  "signals.py" file under "stock" app and add 👇

```python
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction, Product

@receiver(pre_save, sender=Transaction)
def calculate_total_price(sender, instance, **kwargs):
    if not instance.price_total:
        instance.price_total = instance.quantity * instance.price

@receiver(post_save, sender=Transaction)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    if instance.transaction == 1:
        if not product.stock:
            product.stock = instance.quantity
        else:
           product.stock += instance.quantity
    else:
        product.stock -= instance.quantity

    product.save()

```

## 🚩 For the "signal.py" file to work, we need to add the "ready" method to the "apps.py" file 👇

```python
    def ready(self):
        import stock.signals
```

## 🚩 Go to "views.py" and start to write views 👇

```python
from rest_framework import viewsets, filters
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ''
    filter_fields = [filters.SearchFilter]
    search_fields = ['name']
```

## 🚩 Create "serializers.py" under "stock" app 👇

```python
from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )
```

## 🚩 Go back "views.py" and improt that serializer 👇

```python
from .serializers import(
    CategorySerializers,
)
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
```

## 🚩 Create "urls.py" file under "stock" app and add 👇

```python
from django import urls
from django.urls import path
from .views import(
    CategoryView
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Category', CategoryView)

urlpatterns = [

] + router.urls
```

## 🚩 Go to views.py and create BrandView 👇

```python
class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
```

```python
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name"
        )
```

```python
router.register('Brand', BrandView)
```

```python
from django_filters.rest_framework import DjangoFilterBackend

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']
```

## ✔ Add 'django_filters' to the INSTALLED_APP in "settings.py" 👇

```python
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "stock"
        )

        read_only_fields = ('stock',)
```

```python
router.register('product', ProductView)
```













## 🚩 Go to "main/urls.py" and add the path 👇

```python
path('users/', include('users.urls'))
```

## ✔ Create "urls.py" file under "users" App 👇

## 🚩 Go to "users/urls.py" and add 👇

```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
]
```

## 💻 Migrate your database

```bash
python manage.py migrate
```

## ✔ Create "serializers.py" file under "users" App and add 👇

```python
from rest_framework import serializers, validators
# from django.contrib.auth.models import User
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}

    )

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password1'
        )

    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError(
                {"password": "Password didn't match..... "}
            )
        return data

    #! To create a user when the user is registered 👇
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop('password1')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

```

## 🚩 Go to "views.py"

```python
from operator import ge
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
```

## 🚩 Go to "urls.py" and add the path 👇

```python
path('register/', RegisterView.as_view()),
```

## 🚩 Go to "base.py" and add 👇

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

## 🚩 Create "signals.py" under "user" App and add 👇

```python
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

## 🚩 Go to "apps.py" and add this under UsersConfig() 👇

```python
def ready(self) -> None:
    import users.signals
```

## 🚩 Go to "views.py" and customize RegisterView()👇

```python
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    #! When user register 👉 "username", "email","first_name","last_name" and "token" will be returned. 👇
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User does not have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

## 🚩 Override TokenSerializer() 👇

```python
from dj_rest_auth.serializers import TokenSerializer

#! We need to override the TokenSerializer to return all user data in a single request.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {
            'username',
            'email'
        }

class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = {
            'key',
            'user'
        }
```

## 🚩 Go to "base.py" and add 👇

```python
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.CustomTokenSerializer',
}
```

## <center> ****************************************************** </center>

# <center> 🚀 LOGIC STARTING </center>

- Flights:
    + Users:

        - views upcoming flights
    
    + Staff members:
        - views all flights with reservations
        - create flights

- Reservations :
    + Login_users:
        - create reservations:
        - views only their reservations

    + Staff_users:
        - create reservations
        - views all reservations

## 🚩 ADDING AN APP:

💻 Go to terminal 👇

```bash
python manage.py startapp flight
```

✔ Go to "base.py" and add 'users' app to "INSTALLED_APPS"

## 🚩 Go to "flight/models.py" and create Models 👇

```python
from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    operating_airlines = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=20)
    arrival_city = models.CharField(max_length=20)
    date_of_departure = models.DateField()
    etd = models.TimeField()

    def __str__(self):
        return f'{self.flight_number} - {self.departure_city} - {self.arrival_city}'

class Passenger(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    passenger = models.ManyToManyField(Passenger, related_name = 'reservations')
    #! 👆 It is possible to access the parent table that is related to via related_name. 👉 p.reservations.all()
    flight = models.ForeignKey(Flight, on_delete = models.CASCADE, related_name="reservation")
```

## 🚩 Register the models in "flight/admin.py" 👇

```python
from django.contrib import admin
from .models import Flight, Passenger, Reservation

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Reservation)
```

## 💻 Go to terminal for migration 👇

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🚩 Create "serializers.py" file under "flight" App 👇

```python
from rest_framework import serializers
from .models import Flight, Passenger, Reservation

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "flight_number",
            "operating_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )
```

## 🚩 Time to add views in "flight/views.py" 👇

```python
from django.shortcuts import render
from .serializers import FlightSerializer
from rest_framework import viewsets
from .models import Flight, Passenger, Reservation

#! Thanks to the modelviewset, we can do all the operations 👇
#!  GET, POST, PUT, DELETE, PATCH
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
```

## 🚩 Go to "main/urls.py" and add the path 👇

```python
path('flight/', include('flight.urls'))
```

## 🚩 Create "urls.py" file under "flight" App 👇

```python
from rest_framework import routers
from .views import FlightView

router = routers.DefaultRouter()
router.register('flights', FlightView)

urlpatterns = [

]

urlpatterns += router.urls
```

## 🚩 We will use "IsAdminUser" so that only the authorized user can create a flight. For that create "permissions.py" file under "flight" App 👇

```python
from rest_framework import permissions

class IsStafforReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
```

## 🚩 Go to "views.py" and add this permission 👇

```python
from .permissions import IsStafforReadOnly

class FlightView(viewsets.ModelViewSet):

    permission_classes = (IsStafforReadOnly,)
```

## 🚩 Go to "serializers.py" and add ReservationSerializer() 👇

```python
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "flight",  # GET
            "flight_id",  # POST
            "user",  # GET
            "user_id",  # POST
            "passenger"
        )
```

## 🚩 Go to "views.py" and add ReservationView() 👇

```python
from .serializers import ReservationSerializer
class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
```

## 🚩 Go to "flight/urls.py" and add the path 👇

```python
from .views import ReservationView
router.register('resv', ReservationView)
```

## 🚩 Go to "serializers.py" and add PassengerSerializer() 👇

```python
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"
```

## 🚩 In ReservationSerializer() add 👇

```python
passenger = PassengerSerializer(many = True, required=True)
flight = serializers.StringRelatedField()
flight_id = serializers.IntegerField(write_only=True)
#! write_only 👉 It will only appear when creating
user = serializers.StringRelatedField()
user_id = serializers.IntegerField(write_only=True, required=False)
```

## 🚩 We need to extract passenger information from the data, when the reservation is created. For that add to "serializers.py" 👇

```python
def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')
        validated_data['user_id'] = self.context['request'].user.id
        # We updated the user information inside data 👆
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation
```

## 🚩 All reservation information can only be seen by the staff user <i>(Users will only see their own reservation)</i>. For that override "get_queryset" method in "ReservationView()" in "views.py" 👇

```python
  #! Overriding "get_queryset" Method 👇
 def get_queryset(self):
        queryset = super().get_queryset() # 👉 Reservation.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user = self.request.user)
```

## 🚩 Let the staff members see the reservation information of that flight for each flight. For this, we will add reservations to "FlightView()" by writing a separate serializer and say show it to staff 👇

```python
class StaffFlightSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"
```

## 🚩 Go to "views.py" and override "get_serializer_class" in "FlightView()" 👇

```python
from .serializers import StaffFlightSerializer
def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer
```

## 🚩 We will override the "get_query_set" method in "FlightView()" so that normal users can't see past flights 👇

```python
from datetime import datetime, date
def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()

        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            queryset = Flight.objects.filter(date_of_departure__gt = today)
            if Flight.objects.filter(date_of_departure = today):
                today_qs = Flight.objects.filter(date_of_departure = today).filter(etd__gt=current_time)
            queryset = queryset.union(today_qs)
            return queryset
```

## 📢 Do not forget to check the endpoints you wrote in [Postman](https://www.postman.com/).

## <center>🥳 END OF THE  PROJECT 🥳</center>