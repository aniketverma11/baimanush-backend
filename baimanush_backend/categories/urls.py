from django.urls import path, include

from baimanush_backend.categories.api.v1.views import (
    CategoryViewSet,
    SubCategoryViewSet,
)


urlpatterns = [
    path("categories/", CategoryViewSet.as_view({"get": "get"}))
]
