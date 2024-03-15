from rest_framework import viewsets, status
from baimanush_backend.categories.models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer

from baimanush_backend.utils.response import cached_response


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Category.objects.prefetch_related("subcategory_set").all()
    serializer_class = CategorySerializer

    def get(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )


class SubCategoryViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )
