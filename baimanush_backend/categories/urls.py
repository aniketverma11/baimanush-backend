from django.urls import path, include

from rest_framework.routers import DefaultRouter

from baimanush_backend.categories.api.v1.views import (
    CategoryViewSet,
    SubCategoryViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"subcategories", SubCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("categories/", CategoryViewSet.as_view({"get": "get"})),
    path("subcategories/", SubCategoryViewSet.as_view({"get": "get"})),
]
