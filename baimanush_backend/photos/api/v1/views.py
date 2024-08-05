from rest_framework import viewsets, status
from baimanush_backend.utils.response import cached_response
from rest_framework.permissions import IsAuthenticated

from baimanush_backend.photos.models import Photos, Photos_Images
from .serializers import (
    PhotosDetailSerializer,
    ImagesSerializer,
    PhotoslistSerializer,
    PhotosRssFeedSerializer
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PhotosViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Photos.objects.filter(
        is_deleted=False, is_for_members=False, is_draft=False
    ).order_by(
        "-publish"
    )  # Photos.objects.prefetch_related('images_set').all()
    serializer_class = PhotoslistSerializer

    def list(self, request):
        type = request.GET.get("type")
        if type:
            photos = self.queryset.filter(type=type)
            serializer = PhotoslistSerializer(photos, many=True)

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

    def get(self, request, slug):
        type = request.GET.get("type")
        if type:
            photo = (
                self.queryset.prefetch_related("photos_images_set")
                .filter(slug=slug)
                .first()
            )
            try:
                photo.views_count += 1
                photo.save()
            except Exception:
                pass

            serializer = PhotosDetailSerializer(photo, context={"request": request})

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

    def most_viewed(self, request):
        type = request.GET.get("type")
        if type:
            try:
                articles = self.queryset.filter(type=type).order_by("-views_count")[:10]
            except Photos.DoesNotExist:
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
    
    def rss_feed_list(self, request, category_slug):
        type = request.GET.get("type")
        if type:
            # try:
            
            photos = self.queryset.filter(
                type=type
            ).order_by("-publish")


            paginator = Paginator(photos, 10)  # Show 10 articles per page
            page = request.GET.get('page')

            try:
                paged_articles = paginator.page(page)
            except PageNotAnInteger:
                paged_articles = paginator.page(1)
            except EmptyPage:
                paged_articles = paginator.page(paginator.num_pages)

            serializer = PhotosRssFeedSerializer(
                paged_articles, many=True, context={"request": request}
            )

            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={
                    "page": paged_articles.number,
                    "pages": paginator.num_pages,
                    "total": paginator.count,
                    "has_next": paged_articles.has_next(),
                    "has_previous": paged_articles.has_previous()
                },
            )

