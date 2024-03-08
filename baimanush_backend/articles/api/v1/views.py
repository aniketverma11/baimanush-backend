from rest_framework import viewsets, status
from rest_framework.response import Response

from baimanush_backend.utils.response import cached_response
from baimanush_backend.articles.models import Post, SubscribeMail, Reference
from baimanush_backend.categories.models import Category, SubCategory
from baimanush_backend.articles.api.v1.serializers import *

class PostListViewset(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.filter(is_deleted=False, is_for_members=False).order_by("-created")

    




