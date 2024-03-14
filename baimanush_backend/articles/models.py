from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from baimanush_backend.utils.behaviours import *
from baimanush_backend.categories.models import *

class Reference(SlugMixin, StatusMixin, TimeStampedModel):
	title = models.CharField('Title', max_length=512, blank=True, null=True)
	url = models.URLField('url', blank=False, null=False)

	def __str__(self):
		return str(self.url)
class Tag(SlugMixin, StatusMixin, TimeStampedModel):
    tag = models.CharField(_('Tag'), max_length=255, blank=False, null=False,
                                      validators=[validator_ascii])

    def __str__(self):
        return self.tag
	
class Post(PostMixin, UserStampedMixin):
	category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
	minutes_read = models.PositiveIntegerField("Minutes Read", default=5, blank=False, null=False)
	references = models.ManyToManyField(Reference, blank=True)
	sub_categories = models.ManyToManyField(SubCategory, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	author = models.CharField(_("Author"), max_length=50, blank=True)
	is_for_members = models.BooleanField(_("Members Only"), default=False)
	home_screen =  models.BooleanField(_("For main grid"), default=False)
	is_draft = models.BooleanField(_("Draft"), default=True)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse("blog:blog_detail", kwargs={"slug": self.slug})


class SubscribeMail(StatusMixin, TimeStampedModel):
    mail = models.EmailField(blank=True, null=True)

    def __str__(self):
        return str(self.mail)


