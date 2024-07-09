from rest_framework import serializers
from baimanush_backend.videos.models import Video
from baimanush_backend.categories.api.v1.serializers import (
    CategoryListSerializer,
    SubcategoryListSerializer,
)
from baimanush_backend.articles.api.v1.serializers import TagSerializer


class VideoListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    category = CategoryListSerializer()
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        queryset = queryset.select_related("category")
        return queryset

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return ""

    def get_title(self, obj):
        if obj.title:
            return obj.title[:125]
        return ""

    def get_category(self, obj):
        if obj.category:
            return obj.category.slug
        return ""

    def get_short_description(self, obj):
        if obj.short_description:
            return ""  # obj.short_description[:200] + '...'
        return ""

    def get_content(self, obj):
        if obj.content:
            return obj.content[:200] + "...</p>"
        return ""

    class Meta:
        model = Video
        fields = (
            "slug",
            "title",
            "short_description",
            "video",
            "content",
            "image",
            "image_description",
            "category",
            "tags",
            "author",
            "publish",
        )


class VideoDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    tags = TagSerializer(many=True)
    read_more = serializers.SerializerMethodField()
    treanding_news = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = "__all__"

    def get_read_more(self, obj):
        # Fetch additional data for "read_more" here
        # Assuming read_more_data is a list of additional data
        request = self.context.get("request")
        type_param = request.GET.get("type")
        read_more_data = (
            Video.objects.filter(is_deleted=False, is_draft=False, type=type_param)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        read_more_serializer = VideoListSerializer(read_more_data, many=True)
        return read_more_serializer.data

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return ""

    def get_treanding_news(self, obj):
        request = self.context.get("request")
        type_param = request.GET.get("type")
        trending = (
            Video.objects.filter(is_trending=True, is_deleted=False, is_draft=False, type=type_param)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        trending_serializer = VideoListSerializer(trending, many=True)
        return trending_serializer.data


