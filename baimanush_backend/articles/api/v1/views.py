from rest_framework import viewsets, status
from rest_framework.response import Response

from baimanush_backend.utils.response import cached_response
from baimanush_backend.articles.models import Post, SubscribeMail, Reference
from baimanush_backend.categories.models import Category, SubCategory
from baimanush_backend.articles.api.v1.serializers import *

class PostListViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.filter(is_deleted=False, is_for_members=False, is_draft=False).order_by("-publish")
    serializer_class = PostListSerializer

    def home_screen_content(self, request):
        try:
            articles = self.queryset.filter(home_screen=True).order_by('-publish')[:8]
        except Post.DoesNotExist:
            articles = []

        serializer = self.serializer_class(articles, many=True)
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )


class PostDetailViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.filter(is_deleted=False, is_for_members=False, is_draft=False).order_by("-created")
    serializer_class = PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        category_slug = kwargs.get('category_slug')
        slug = kwargs.get('slug')
        

        article = self.queryset.filter(category__slug=category_slug, slug=slug).first()

        if article:
            serializer = PostDetailSerializer(article)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        
        article = self.queryset.filter(slug=slug).first()
        serializer = PostDetailSerializer(article)
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )



