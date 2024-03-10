from rest_framework import serializers
from baimanush_backend.articles.models import Post


class PostListSerializer(serializers.ModelSerializer):
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

    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(obj.image.url)
    #     return ''

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description[:200] + '...'
        return ''

    class Meta:
        model = Post
        fields = ('slug', 'short_description', 'title', 'image', 'image_alt', 'category', 'tags', 'user')


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'