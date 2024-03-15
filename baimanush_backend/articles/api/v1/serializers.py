from rest_framework import serializers
from baimanush_backend.articles.models import Post, Tag, Reference
from baimanush_backend.categories.api.v1.serializers import CategoryListSerializer, SubcategoryListSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["slug", "tag"]

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ["slug", "title", "url"]

class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    short_description = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)


    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('category')
        return queryset

    # def get_category(self, obj):
    #     if obj.category:
    #         return obj.category.slug
    #     return ''

    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(obj.image.url)
    #     return ''

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description
        return ''

    class Meta:
        model = Post
        fields = ('slug', 'short_description', 'title', 'image', 'image_alt', 'category', 'tags', 'created_by', "author")


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    references = ReferenceSerializer(many=True)
    class Meta:
        model = Post
        fields = '__all__'
    
    