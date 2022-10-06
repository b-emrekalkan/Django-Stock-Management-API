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