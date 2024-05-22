from rest_framework import serializers

from ..models import PostComments, PhotoComments, VideoComments

from baimanush_backend.users.api.serializers import UserProfileSerializer
from baimanush_backend.articles.api.v1.serializers import PostListSerializer


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = PostComments
        fields = "__all__"

class PostCommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()

class PhotosCommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()

class VideoCommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()

class PhotosCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = PhotoComments
        fields = "__all__"


class VideosCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = VideoComments
        fields = "__all__"
