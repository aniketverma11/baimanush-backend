from rest_framework import viewsets, status
from rest_framework.response import Response

from baimanush_backend.utils.response import cached_response
from baimanush_backend.videos.models import Video
from baimanush_backend.categories.models import Category, SubCategory
from baimanush_backend.videos.api.v1.serializers import *

class VideoListViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Video.objects.filter(is_deleted=False, is_for_members=False, is_draft=False).order_by("-created")
    serializer_class = VideoListSerializer

    def list(self, request):
        try:
            videos = self.queryset.order_by('-modified')
        except Video.DoesNotExist:
            videos = []

        serializer = self.serializer_class(videos, many=True)
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer.data,
            meta={},
        )
    
    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        
        article = self.queryset.filter(slug=slug).first()

        if article:
            serializer = VideoDetailSerializer(article)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        else:
            return cached_response(
                request=request,
                status=status.HTTP_400_BAD_REQUEST,
                response_status="failed",
                message="post not found",
                data={},
                meta={},
            )