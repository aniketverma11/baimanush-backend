from rest_framework import viewsets
from baimanush_backend.categories.models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset =  Category.objects.prefetch_related('subcategory_set').all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer