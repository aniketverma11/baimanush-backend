from rest_framework import serializers
from baimanush_backend.articles.models import Post, Tag, Reference, PostComments
from baimanush_backend.categories.api.v1.serializers import (
    CategoryListSerializer,
    SubcategoryListSerializer,
)
from baimanush_backend.categories.models import Category

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["slug", "tag"]


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ["slug", "title", "url"]

class PostListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    def get_audio(self, obj):
        if obj.audio:
            return obj.audio.url 
        return ''

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        queryset = queryset.select_related("category")
        return queryset

    def get_title(self, obj):
        if obj.title:
            return obj.title[:50] + "..."
        return ""

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description[:200] + "..."
        return ""

    def get_content(self, obj):
        if obj.content:
            return obj.content[:200] + "...</p>"
        return ""

    def get_category(self, obj):
        request = self.context.get("request")
        type_param = request.GET.get("type")
        category = obj.category

        if not type_param != "english":
            serializer = CategoryListSerializer(category, context={"request": request})
            return serializer.data
        else:
            return {
                "name": category.marathi_name,
                "slug": category.slug,
            }

    class Meta:
        model = Post
        fields = (
            "slug",
            "short_description",
            "title",
            "content",
            "image",
            "image_description",
            "category",
            "tags",
            "created_by",
            "author",
            "publish",
        )

class PostDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    sub_categories = SubcategoryListSerializer(many=True)
    tags = TagSerializer(many=True)
    references = ReferenceSerializer(many=True)
    read_more = serializers.SerializerMethodField()
    treanding_news = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    def get_audio(self, obj):
        if obj.audio:
            return obj.audio.url 
        return ''

    def get_read_more(self, obj):
        # Fetch additional data for "read_more" here
        # Assuming read_more_data is a list of additional data
        request = self.context.get("request")
        type_param = request.GET.get("type")
        request = self.context.get("request")
        read_more_data = (
            Post.objects.filter(is_deleted=False, is_draft=False, type=type_param)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        read_more_serializer = PostListSerializer(
            read_more_data, many=True, context={"request": request}
        )
        return read_more_serializer.data

    def get_treanding_news(self, obj):
        request = self.context.get("request")
        trending = (
            Post.objects.filter(is_trending=True, is_deleted=False, is_draft=False)
            .exclude(slug=obj.slug)
            .order_by("-publish")[:4]
        )  # Fetch read_more data as needed
        trending_serializer = PostListSerializer(
            trending, many=True, context={"request": request}
        )
        return trending_serializer.data

    def get_category(self, obj):
        request = self.context.get("request")
        type_param = request.GET.get("type")
        category = obj.category

        if not type_param != "english":
            serializer = CategoryListSerializer(category, context={"request": request})
            return serializer.data
        else:
            return {
                "name": category.marathi_name,
                "slug": category.slug,
            }

class MemberOnlyListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url 
        return ''

    def get_audio(self, obj):
        if obj.audio:
            return obj.audio.url 
        return ''

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        queryset = queryset.select_related("category")
        return queryset

    def get_short_description(self, obj):
        if obj.short_description:
            return obj.short_description[:200] + "..."
        return ""

    def get_category(self, obj):
        request = self.context.get("request")
        type_param = request.GET.get("type")
        category = obj.category

        if not type_param != "english":
            serializer = CategoryListSerializer(category, context={"request": request})
            return serializer.data
        else:
            return {
                "name": category.marathi_name,
                "slug": category.slug,
            }

    def get_title(self, obj):
        if obj.title:
            return obj.short_title[:50] + "..."
        return ""

    class Meta:
        model = Post
        fields = (
            "slug",
            "short_description",
            "title",
            "image",
            "image_description",
            "category",
            "tags",
            "created_by",
            "author",
            "publish",
        )

class CategoryPostListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    category = CategoryListSerializer()
    short_description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        queryset = queryset.select_related("category")
        return queryset

    def get_short_description(self, obj):
        if obj.short_description:
            return ""  # obj.short_description[:200] + '...'
        return ""

    def get_title(self, obj):
        if obj.title:
            return obj.title[:75] + "..."
        return ""

    def get_content(self, obj):
        if obj.content:
            return obj.content[:200] + "...</p>"
        return ""

    class Meta:
        model = Post
        fields = (
            "slug",
            "short_description",
            "title",
            "content",
            "image",
            "image_description",
            "category",
            "tags",
            "created_by",
            "author",
            "publish",
        )

class CategoryArticlesSerializer(serializers.ModelSerializer):
    posts = CategoryPostListSerializer(many=True, source="post_set")

    class Meta:
        model = Category
        fields = "__all__"

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComments
        fields = "__all__"
