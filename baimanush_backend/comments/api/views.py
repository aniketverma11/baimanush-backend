from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from baimanush_backend.utils.response import cached_response

from ..models import PostComments, PhotoComments, VideoComments
from .serializers import *

from baimanush_backend.articles.models import Post
from baimanush_backend.photos.models import Photos
from baimanush_backend.videos.models import Video


class PostCommentsViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = []
    serializer_class = PostCommentSerializer
    queryset = PostComments.objects.filter(is_active=True, is_deleted=False)

    def create(self, request, post_slug):
        print("ok")
        data = request.data
        user = request.user
        print(user, "----------------")

        serializer = PostCommentCreateSerializer(data=data)

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
            data=self.serializer_class(comment).data,
            meta={},
        )
    
    
class PostCommentListViewset(viewsets.ViewSet):
    permission_classes = []
    serializer_class = PostCommentSerializer
    queryset = PostComments.objects.filter(is_active=True, is_deleted=False)

    def list(self, request, post_slug):
        if post_slug:
            comments = self.queryset.filter(post__slug=post_slug)
            serializer = self.serializer_class(comments, many=True)
            return cached_response(
                request=request,
                status=status.HTTP_200_OK,
                response_status="success",
                message="List of comments",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="Post Slug is required",
            data={},
            meta={},
        )
    
class PhotoCommentsViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotosCommentSerializer
    queryset = PhotoComments.objects.filter(is_active=True, is_deleted=False)

    def create(self, request, post_slug):
        data = request.data
        user = request.user

        serializer = PhotosCommentCreateSerializer(data=data)

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
            data=self.serializer_class(comment).data,
            meta={},
        )
    
class PhotoCommentsListViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotosCommentSerializer
    queryset = PhotoComments.objects.filter(is_active=True, is_deleted=False)

    def list(self, request, photos_slug):
        if photos_slug:
            comments = self.queryset.filter(post__slug=photos_slug)
            serializer = self.serializer_class(comments, many=True)
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
            message="Post Slug is required",
            data={},
            meta={},
        )


class CommentsViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = VideosCommentSerializer
    queryset = VideoComments.objects.filter(is_active=True, is_deleted=False)


    def create(self, request, post_slug):
        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            content = serializer.data["content"]

        try:
            post = Video.objects.get(slug=post_slug)
            comment = VideoComments.objects.create(
                user=user, video=post, content=content
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
            data=self.serializer_class(comment).data,
            meta={},
        )


class CommentsListViewset(viewsets.ViewSet):
    permission_classes = ()
    serializer_class = VideosCommentSerializer
    queryset = VideoComments.objects.filter(is_active=True, is_deleted=False)

    def list(self, request, video_slug):
        if video_slug:
            comments = self.queryset.filter(post__slug=video_slug)
            serializer = self.serializer_class(comments, many=True)
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
            message="Post Slug is required",
            data={},
            meta={},
        )