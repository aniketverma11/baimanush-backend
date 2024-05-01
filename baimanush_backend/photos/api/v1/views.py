from rest_framework import viewsets, status
from baimanush_backend.utils.response import cached_response
from rest_framework.permissions import IsAuthenticated

from baimanush_backend.photos.models import Photos, Photos_Images, PhotoComments
from .serializers import (
    PhotosDetailSerializer,
    ImagesSerializer,
    PhotoslistSerializer,
    PhotosCommentSerializer,
)


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


class PhotoCommentsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotosCommentSerializer

    def create(self, request, post_slug):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data)

        if serializer.is_valid(raise_exception=True):
            content = serializer.data["content"]

        try:
            post = Photos.objects.get(slug=post_slug)
            comment = PhotoComments.objects.create(
                user=user, photo=post, content=content
            )
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
