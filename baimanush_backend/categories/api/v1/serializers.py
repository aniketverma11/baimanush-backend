from rest_framework import serializers
from baimanush_backend.categories.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        # if request and 'type' in request.GET:
        type_param = request.GET.get("type")
        if not type_param != "english":
            return {
                "name": instance.name,
                "slug": instance.slug,
                "marathi_name": instance.marathi_name,
            }
        if type_param =='dharitri-english':
                return {
                    "name": instance.name,
                    "slug": instance.slug,
                }
        return {
            "name": instance.marathi_name,
            "slug": instance.slug,
        }

    class Meta:
        model = Category
        fields = ["slug", "name", "marathi_name"]


class SubcategoryListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = SubCategory
        fields = ["slug", "name"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name", "marathi_name"]
