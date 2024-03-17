from rest_framework import serializers
from baimanush_backend.photos.models import Photos, Images
from baimanush_backend.categories.api.v1.serializers import (
    CategoryListSerializer,
    SubcategoryListSerializer,
)
from baimanush_backend.articles.api.v1.serializers import TagSerializer


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class PhotoslistSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, source="images_set")
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Photos
        fields = "__all__"


class PhotosDetailSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, source="images_set")
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    read_more = serializers.SerializerMethodField()
    treanding_news = serializers.SerializerMethodField()

    class Meta:
        model = Photos
        fields = "__all__"

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return ""

    def get_read_more(self, obj):
        # Fetch additional data for "read_more" here
        # Assuming read_more_data is a list of additional data
        read_more_data = (
            Photos.objects.filter(is_deleted=False, is_draft=False)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        read_more_serializer = PhotoslistSerializer(read_more_data, many=True)
        return read_more_serializer.data

    def get_treanding_news(self, obj):
        trending = (
            Photos.objects.filter(is_trending=True)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        trending_serializer = PhotoslistSerializer(trending, many=True)
        return trending_serializer.data
