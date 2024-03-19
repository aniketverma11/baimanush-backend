from rest_framework import viewsets, status
from baimanush_backend.utils.response import cached_response

from baimanush_backend.photos.models import Photos, Photos_Images
from .serializers import PhotosDetailSerializer, ImagesSerializer, PhotoslistSerializer


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
        serializer = PhotoslistSerializer(self.queryset, many=True)

        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )

    def get(self, request, slug):
        photo = self.queryset.prefetch_related("images_set").filter(slug=slug).first()
        serializer = PhotosDetailSerializer(photo)

        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )
