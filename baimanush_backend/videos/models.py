from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ckeditor.fields import RichTextField

from baimanush_backend.utils.behaviours import *
from baimanush_backend.categories.models import *

# Create your models here.
class Video(SlugMixin, StatusMixin, TimeStampedModel, UserStampedMixin):
    video = RichTextField(config_name='allow_iframes')
    title = models.CharField(_("title"), max_length=255, null=False, blank=False, validators=[validator_ascii])
    short_description = models.TextField(_("short description"), max_length=500, blank=True, validators=[validator_ascii])
    content = RichTextUploadingField(_("content"), blank=True, null=True)
    publish = models.DateTimeField(_("publish datetime"), auto_now=False, auto_now_add=False, default=timezone.now)
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    minutes_read = models.PositiveIntegerField("Minutes Read", default=5, blank=False, null=False)
    sub_categories = models.ManyToManyField(SubCategory)
    author = models.CharField(_("Author"), max_length=50, blank=True)
    is_for_members = models.BooleanField(_("Members Only"), default=False)
    is_draft = models.BooleanField(_("Draft"), default=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"slug": self.slug})
    

    
