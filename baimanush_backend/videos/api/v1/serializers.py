from rest_framework import serializers
from baimanush_backend.videos.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

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
            return obj.short_description[:200] + '...'
        return ''

    class Meta:
        model = Video
        fields = ('slug', 'short_description', 'title', 'image', 'image_alt', 'category', 'tags', 'author')


class VideoDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        return ''