from django.db import models

from baimanush_backend.utils.behaviours import *

from baimanush_backend.articles.models import Post
from baimanush_backend.photos.models import Photos
from baimanush_backend.videos.models import Video

class BookMarks(UUIDMixin, UserStampedMixin, StatusMixin):
    articles = models.ManyToManyField(Post)
    videos = models.ManyToManyField(Video)
    photos = models.ManyToManyField(Photos)

    
    class Meta:
        verbose_name = "Bookmarks"
        verbose_name_plural = "Bookmarks"