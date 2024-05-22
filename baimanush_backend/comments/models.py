from django.db import models
from baimanush_backend.utils.behaviours import *

from baimanush_backend.articles.models import Post
from baimanush_backend.photos.models import Photos
from baimanush_backend.videos.models import Video



class PostComments(SlugMixin, UserStampedMixin, CommentMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Post Comment"
        verbose_name_plural = "Post Comments"


class PhotoComments(SlugMixin, UserStampedMixin, CommentMixin):
    photo = models.ForeignKey(Photos, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Photos Comment"
        verbose_name_plural = "Photos Comments"

class VideoComments(SlugMixin, UserStampedMixin, CommentMixin):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Post Comment"
        verbose_name_plural = "Post Comments"
