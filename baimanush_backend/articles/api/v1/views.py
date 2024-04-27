from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from baimanush_backend.utils.response import cached_response
from baimanush_backend.articles.models import Post, SubscribeMail, Reference
from baimanush_backend.categories.models import Category, SubCategory
from baimanush_backend.articles.api.v1.serializers import *


class PostListViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.filter(
        is_deleted=False, is_for_members=False, is_draft=False
    ).order_by("-publish")
    serializer_class = PostListSerializer

    def home_screen_content(self, request):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(home_screen=True, type=type).order_by(
                    "-publish"
                )[:8]
            except Post.DoesNotExist:
                articles = []

            serializer = self.serializer_class(
                articles, many=True, context={"request": request}
            )
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def article_list_via_category(self, request):
        type = request.GET.get("type")
        if type:
            try:
                categories = Category.objects.prefetch_related("post_set").all().order_by('-created')
            except Category.DoesNotExist:
                categories = []

            articles = []
            for category in categories:
                category_data = CategoryArticlesSerializer(
                    category, context={"request": request}
                ).data
                if type:
                    filtered_posts = category.post_set.filter(type=type).order_by(
                        "-publish"
                    )[:3]
                else:
                    filtered_posts = category.post_set.all().order_by("-publish")[:3]
                category_data["posts"] = CategoryPostListSerializer(
                    filtered_posts, many=True, context={"request": request}
                ).data
                articles.append(category_data)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=articles,
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def all_article_list_via_category(self, request, category_slug):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(
                    category__slug=category_slug, type=type
                ).order_by("-publish")
            except Post.DoesNotExist:
                articles = []

            serializer = self.serializer_class(
                articles, many=True, context={"request": request}
            )
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def is_member_only_posts(self, request):
        type = request.GET.get("type")
        if type:
            try:
                articles = Post.objects.filter(
                    is_deleted=False, is_for_members=True, is_draft=False, type=type
                ).order_by("-publish")
                print("-------------------", articles)
            except Post.DoesNotExist:
                articles = []

            serializer = MemberOnlyListSerializer(articles, many=True)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def trending_posts(self, request):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(is_trending=True, type=type).order_by(
                    "-publish"
                )[:8]
            except Post.DoesNotExist:
                articles = []

            serializer = self.serializer_class(
                articles, many=True, context={"request": request}
            )
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def search_articles(self, request):
        type = request.GET.get("type")
        query = request.GET.get("q")
        if type:
            try:
                posts = self.queryset.filter(
                    type=type, title__icontains=query
                ).order_by("-publish")
            except Exception:
                posts = self.queryset.filter(type=type).order_by("-publish")[:20]

            serializer = self.serializer_class(
                posts, many=True, context={"request": request}
            )
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )


class PostDetailViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.filter(
        is_deleted=False, is_for_members=False, is_draft=False
    ).order_by("-publish")
    serializer_class = PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        type = request.GET.get("type")
        if type:
            category_slug = kwargs.get("category_slug")
            slug = kwargs.get("slug")

            article = self.queryset.filter(
                category__slug=category_slug, slug=slug, type=type
            ).first()

            if article:
                serializer = PostDetailSerializer(article, context={"request": request})
                return cached_response(
                    request=request,
                    status=status.HTTP_200_OK,
                    response_status="success",
                    message="",
                    data=serializer.data,
                    meta={},
                )

            article = self.queryset.filter(slug=slug, type=type).first()
            if article:
                serializer = PostDetailSerializer(article, context={"request": request})
                return cached_response(
                    request=request,
                    status=status.HTTP_200_OK,
                    response_status="success",
                    message="",
                    data=serializer.data,
                    meta={},
                )
            return cached_response(
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
                response_status="success",
                message="Post not found with this category",
                data={},
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )

    def retrieve_by_slug(self, request, *args, **kwargs):
        type = request.GET.get("type")
        if type:
            slug = kwargs.get("slug")

            article = self.queryset.filter(slug=slug, type=type).first()

            if article:
                serializer = PostDetailSerializer(article, context={"request": request})
                return cached_response(
                    request=request,
                    status=status.HTTP_200_OK,
                    response_status="success",
                    message="",
                    data=serializer.data,
                    meta={},
                )

            article = self.queryset.filter(slug=slug, type=type).first()
            serializer = PostDetailSerializer(article)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="success",
            message="Type is required",
            data={},
            meta={},
        )


class MemberPostDetailViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.filter(
        is_deleted=False, is_for_members=False, is_draft=False
    ).order_by("-publish")
    serializer_class = PostDetailSerializer

    def member_only_post(self, request, slug):
        article = Post.objects.filter(
            is_for_members=True, slug=slug, is_deleted=False, is_draft=False
        ).first()

        if article:
            serializer = PostDetailSerializer(article, context={"request": request})
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="hello",
                data=serializer.data,
                meta={},
            )
        else:
            return Response(
                {"message": "Member-only post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostCommentsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCommentSerializer

    def create(self, request, post_slug):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data)

        if serializer.is_valid(raise_exception=True):
            content = serializer.data["content"]

        try:
            post = Post.objects.get(slug=post_slug)
            comment = PostComments.objects.create(user=user, post=post, content=content)
        except Exception:
            return cached_response(
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
                response_status="Failed",
                message="",
                data={},
                meta={},
            )

        return cached_response(
            request=request,
            status=status.HTTP_201_CREATED,
            response_status="success",
            message="comment post successfully",
            data=serializer.data,
            meta={},
        )
