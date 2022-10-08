from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import CustomModelPermission

from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

from .serializers import(
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    FirmSerializer,
    TransactionSerializer,
    CategoryProductsSerializer
)
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ["name"]
    permission_classes = [CustomModelPermission]

    def get_serializer_class(self):
        if self.request.query_params.get('name'):
            return CategoryProductsSerializer
        else:
            return super().get_serializer_class

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [CustomModelPermission]


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']
    permission_classes = [CustomModelPermission]


class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [CustomModelPermission]


class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['firm', 'transaction', 'product']
    search_fields = ['firm']
    permission_classes = [CustomModelPermission]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)