from rest_framework import serializers
from baimanush_backend.videos.models import Video
from baimanush_backend.categories.api.v1.serializers import CategoryListSerializer, SubcategoryListSerializer
from baimanush_backend.articles.api.v1.serializers import TagSerializer


class VideoListSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('category')
        return queryset

    def get_category(self, obj):
        if obj.category:
            return obj.category.slug
        return ''

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description
        return ''

    class Meta:
        model = Video
        fields = ('slug', 'short_description', 'title', 'image', 'image_alt', 'category', 'tags', 'author')


class VideoDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Video
        fields = '__all__'
