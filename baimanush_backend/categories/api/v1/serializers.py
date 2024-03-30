from rest_framework import serializers
from baimanush_backend.categories.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = "__all__"


class SubcategoryListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = SubCategory
        fields = ["slug", "name"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name"]
