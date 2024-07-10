from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from baimanush_backend.utils.response import cached_response
from baimanush_backend.articles.models import Post, SubscribeMail, Reference
from baimanush_backend.categories.models import Category, SubCategory
from baimanush_backend.articles.api.v1.serializers import *

from baimanush_backend.videos.models import Video
from baimanush_backend.videos.api.v1.serializers import VideoListSerializer

from baimanush_backend.photos.models import Photos
from baimanush_backend.photos.api.v1.serializers import PhotoslistSerializer


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
            response_status="failed",
            message="Type is required",
            data={},
            meta={},
        )

    def article_list_via_category(self, request):
        type = request.GET.get("type")
        if type:
            try:
                categories = (
                    Category.objects.prefetch_related("post_set")
                    .all()
                    .order_by("-created")
                )
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
            response_status="failed",
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
            response_status="failed",
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

            serializer = MemberOnlyListSerializer(articles, many=True, context={"request": request})
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
            response_status="failed",
            message="Type is required",
            data={},
            meta={},
        )

    def trending_posts(self, request):
        type = request.GET.get("type")
        if type:
            try:
                article = self.queryset.filter(home_screen=True, type=type).order_by(
                    "-publish"
                ).first()
                articles = self.queryset.filter(is_trending=True, type=type).exclude(slug=article.slug).order_by(
                    "-publish"
                )[:5]
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
            response_status="failed",
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
            response_status="failed",
            message="Type is required",
            data={},
            meta={},
        )

    def most_viewed(self, request):
        type = request.GET.get("type")
        type = request.GET.get("type")
        q = request.GET.get("q")
        if type and q:
            if q == "videos":
                try:
                    articles = Video.objects.filter(
                        is_deleted=False, is_draft=False, type=type
                    ).order_by("-views_count")[:10]
                except Video.DoesNotExist:
                    articles = []
                serializer = VideoListSerializer(
                    articles, many=True, context={"request": request}
                )

            if q == "photos":
                try:
                    articles = Photos.objects.filter(
                        is_deleted=False, is_draft=False, type=type
                    ).order_by("-views_count")[:10]

                except Photos.DoesNotExist:
                    articles = []

                serializer = PhotoslistSerializer(
                    articles, many=True, context={"request": request}
                )

            if q == "posts":
                try:
                    articles = Post.objects.filter(
                        is_deleted=False, is_draft=False, type=type
                    ).order_by("-views_count")[:10]

                except Post.DoesNotExist:
                    articles = []

                serializer = PostListSerializer(
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
            response_status="failed",
            message="Type OR q is required",
            data={},
            meta={},
        )
    
    def rss_feed_list(self, request, category_slug):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(
                    category__slug=category_slug, type=type
                ).order_by("-publish")
            except Post.DoesNotExist:
                articles = []

            serializer = RssFeedSerializer(
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
            response_status="failed",
            message="Type is required",
            data={},
            meta={},
        )
    
    def rss_feed_get(self, request, slug):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(
                    slug=slug, type=type
                ).order_by("-publish").first()
            except Post.DoesNotExist:
                articles = []

            serializer = RssFeedSerializer(
                articles, context={"request": request}
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
            response_status="failed",
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

            try:
                article.views_count += 1
                article.save()
            except Exception:
                pass

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
            try:
                article.views_count += 1
                article.save()
            except Exception:
                pass
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
                response_status="failed",
                message="Post not found with this category",
                data={},
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="Type is required",
            data={},
            meta={},
        )

    def retrieve_by_slug(self, request, *args, **kwargs):
        type = request.GET.get("type")
        if type:
            slug = kwargs.get("slug")

            article = self.queryset.filter(slug=slug, type=type).first()
            try:
                article.views_count += 1
                article.save()
            except Exception:
                pass

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
            response_status="failed",
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
        try:
            article.views_count += 1
            article.save()
        except Exception:
            pass

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


class SubscribeEmailViewset(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SubscribeEmailSerializers

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_201_CREATED,
                response_status="success",
                message="",
                data={},
                meta={},
            )
        
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data={},
            meta={},
        )