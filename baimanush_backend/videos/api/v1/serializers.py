from rest_framework import serializers
from baimanush_backend.videos.models import Video
from baimanush_backend.categories.api.v1.serializers import (
    CategoryListSerializer,
    SubcategoryListSerializer,
)
from baimanush_backend.articles.api.v1.serializers import TagSerializer


class VideoListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        queryset = queryset.select_related("category")
        return queryset

    def get_category(self, obj):
        if obj.category:
            return obj.category.slug
        return ""

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description
        return ""

    class Meta:
        model = Video
        fields = (
            "slug",
            "title",
            "short_description",
            "content",
            "image",
            "image_alt",
            "category",
            "tags",
            "author",
            "publish",
        )


class VideoDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    read_more = serializers.SerializerMethodField()
    treanding_news = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = "__all__"

    def get_read_more(self, obj):
        # Fetch additional data for "read_more" here
        # Assuming read_more_data is a list of additional data
        read_more_data = (
            Video.objects.filter(is_deleted=False, is_draft=False)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        read_more_serializer = VideoListSerializer(read_more_data, many=True)
        return read_more_serializer.data

    def get_treanding_news(self, obj):
        trending = (
            Video.objects.filter(is_trending=True, is_deleted=False, is_draft=False)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        trending_serializer = VideoListSerializer(trending, many=True)
        return trending_serializer.data
