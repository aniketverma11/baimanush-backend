from rest_framework import serializers
from baimanush_backend.categories.models import Category, SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, source='subcategory_set')

    class Meta:
        model = Category
        fields = '__all__'