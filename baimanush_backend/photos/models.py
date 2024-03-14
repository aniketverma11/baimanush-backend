from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from model_utils.models import TimeStampedModel

from baimanush_backend.utils.behaviours import *
from baimanush_backend.categories.models import *
from baimanush_backend.articles.models import Tag


# Create your models here
class Photos(SlugMixin, StatusMixin, TimeStampedModel, UserStampedMixin):
    title = models.CharField(_("title"), max_length=255, null=False, blank=False, validators=[validator_ascii])
    short_description = models.TextField(_("short description"), max_length=500, blank=True, validators=[validator_ascii])
    content = RichTextUploadingField(_("content"), blank=True, null=True)
    publish = models.DateTimeField(_("publish datetime"), auto_now=False, auto_now_add=False, default=timezone.now)
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    minutes_read = models.PositiveIntegerField("Minutes Read", default=5, blank=False, null=False)
    sub_categories = models.ManyToManyField(SubCategory)
    author = models.CharField(_("Author"), max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_for_members = models.BooleanField(_("Members Only"), default=False)
    is_draft = models.BooleanField(_("Draft"), default=True)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

class Images(ImageMixin, StatusMixin, TimeStampedModel):
    photo= models.ForeignKey(Photos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"