from rest_framework import serializers
from baimanush_backend.photos.models import Photos, Photos_Images, PhotoComments
from baimanush_backend.categories.api.v1.serializers import (
    CategoryListSerializer,
    SubcategoryListSerializer,
)
from baimanush_backend.articles.api.v1.serializers import TagSerializer


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photos_Images
        fields = "__all__"
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    


class PhotoslistSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    images = ImagesSerializer(many=True, source="photos_images_set")
    short_description = serializers.SerializerMethodField()
    category = CategoryListSerializer()
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()

    def get_short_description(self, obj):
        if obj.short_description:
            return ""  # obj.short_description[:200] + '...'
        return ""
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    def get_title(self, obj):
        if obj.title:
            return obj.title[:80] + "..."
        return ""

    class Meta:
        model = Photos
        fields = "__all__"


class PhotosDetailSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, source="photos_images_set")
    category = CategoryListSerializer()
    tags = TagSerializer(many=True)
    read_more = serializers.SerializerMethodField()
    treanding_news = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photos
        fields = "__all__"

    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return ""

    def get_read_more(self, obj):
        # Fetch additional data for "read_more" here
        # Assuming read_more_data is a list of additional data
        request = self.context.get("request")
        type_param = request.GET.get("type")
        read_more_data = (
            Photos.objects.filter(is_deleted=False, is_draft=False, type=type_param)
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


class PhotosCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoComments
        fields = "__all__"
