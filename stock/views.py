from rest_framework import viewsets
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

from .serializers import(
    CategorySerializers,
)
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

