import uuid as uuid
from django.db import models

from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from ckeditor_uploader.fields import RichTextUploadingField

from .managers import StatusMixinManager, PostMixinManager
from .utils import upload_location, validator_ascii, validator_pan_no, create_slug


class StatusMixin(models.Model):
    is_active = models.BooleanField(default=True, blank=False, null=False)
    is_deleted = models.BooleanField(default=False, blank=False, null=False)

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class EmailMixin(models.Model):
    email = models.EmailField(max_length=70, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    address = models.TextField(
        _("Address Line 1"),
        max_length=100,
        blank=True,
        null=True,
        validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    )
    state = models.ForeignKey("core.State", models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey("core.City", models.SET_NULL, blank=True, null=True)
    pin_code = models.ForeignKey("core.PINCode", models.SET_NULL, blank=True, null=True)

    def get_address(self):
        address = ""
        if self.address:
            address += self.address
        if self.city and self.city.name:
            address += ", " + self.city.name
            if self.city.state and self.city.state.name:
                address += ", " + self.city.state.name
                if self.city.state.country and self.city.state.country.name:
                    address += ", " + self.city.state.country.name
        if self.pin_code:
            address += " - " + str(self.pin_code.value)

        if address == "":
            return None
        else:
            return "".join([i if ord(i) < 128 else " " for i in address])

    class Meta:
        abstract = True


class MobileMixin(models.Model):
    mobile = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        help_text="Enter a valid 10 digit mobile number.",
    )
    country_code = models.CharField(
        blank=True,
        null=True,
        max_length=5,
        help_text="Enter a valid country code.",
    )

    class Meta:
        abstract = True


class UUIDMixin(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class ProfileMixin(AddressMixin, MobileMixin, StatusMixin, UUIDMixin):
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class UserStampedMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_%(class)s",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="updated_%(class)s",
    )

    class Meta:
        abstract = True


class MetaTagMixin(models.Model):
    meta_title = models.TextField(
        _("Meta Title"), blank=True, null=True
    )
    meta_description = models.TextField(
        _("Meta Description"), blank=True, null=True
    )
    meta_keywords = models.TextField(
        _("Meta Keywords"), blank=True, null=True
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        """
        slug shouldn't have spaces
        """
        if not self.slug:
            self.slug = create_slug(self)
        if self.slug:
            self.slug = self.slug.replace(" ", "")
        super(SlugMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GeoTagMixin(models.Model):
    lat = models.CharField(_("latitude"), blank=True, null=True, max_length=20)
    lng = models.CharField(_("longitude"), blank=True, null=True, max_length=20)

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.ImageField(
        _("image"), upload_to=upload_location, null=False, blank=False
    )
    image_description = models.TextField(
        _("Image Description"), max_length=500, blank=True
    )

    class Meta:
        abstract = True


class PostMixin(SlugMixin, ImageMixin, MetaTagMixin, StatusMixin, TimeStampedModel):
    title = models.CharField(
        _("title"),
        max_length=255,
        null=False,
        blank=False,
    )
    short_description = models.TextField(
        _("short description"), max_length=500, blank=True
    )
    content = RichTextUploadingField(_("content"), blank=True, null=True)
    # tag = models.CharField(_("tag"), max_length=255, null=True, blank=True)
    publish = models.DateTimeField(
        _("publish datetime"), auto_now=False, auto_now_add=False, default=timezone.now
    )

    views_count = models.PositiveIntegerField(_("Views Count"), default=0, blank=True)
    # external_url = models.URLField(_("External URL"), max_length=500, blank=True, null=True)
    objects = PostMixinManager()

    def __str__(self):
        return self.title

    @property
    def get_meta_tags(self):
        # Twitter Tags
        return_string = '<meta name = "twitter:card" content = "summary" />'
        return_string += '<meta property="og:locale" content="en_US" />'
        return_string += '<meta property="og:site_name" content="baimanus" />'
        return_string += '<meta name = "twitter:site" content = "@baimanus" />'

        if self.short_description:
            return_string += (
                '<meta name = "twitter:description" content = "'
                + str(self.short_description)
                + '" />'
            )
        # OG Tags
        return_string += (
            "<meta property='og:url' content='"
            + settings.SITE_URL
            + self.get_absolute_url()
            + "' />"
        )
        return_string += (
            "<meta property='og:description' content='"
            + str(self.meta_description)
            + "' />"
        )
        return_string += "<meta property='og:type' content='article' />"
        # return_string += "<meta property='og:article:published_time' content='" + str(self.publish) + "' />"
        if self.user:
            return_string += (
                "<meta property='og:article:author' content='"
                + str(self.user.first_name)
                + "' />"
            )
        # return_string += "<meta property='og:article:tag' content='" + self.get_concatenated_categories + "' />"
        if self.title:
            return_string += (
                "<meta property='og:title' content='" + str(self.title) + "' />"
            )
            return_string += (
                '<meta name = "twitter:title" content = "' + str(self.title) + '" />'
            )
        if self.image:
            # for https image urls, og:image:secure_url works
            return_string += (
                "<meta property='og:image:secure_url' content='"
                + str(self.image.url)
                + "' >"
            )
            return_string += (
                "<meta property='og:image' content='" + str(self.image.url) + "' >"
            )
            return_string += (
                "<meta property='og:image:height' content='"
                + str(self.image.height)
                + "' >"
            )
            return_string += (
                "<meta property='og:image:width' content='"
                + str(self.image.width)
                + "' >"
            )
            return_string += (
                "<meta property='twitter:image' content='" + str(self.image.url) + "' >"
            )
            return_string += (
                "<meta property='twitter:image:src' content='"
                + str(self.image.url)
                + "' >"
            )

        return return_string

    class Meta:
        abstract = True
        ordering = ["-created", "-modified"]


class CommentMixin(StatusMixin, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True
    )
    content = models.TextField(
        _("content"), blank=True, null=True
    )

    def __str__(self):
        return self.content

    class Meta:
        abstract = True


class LikeMixin(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.user

    class Meta:
        abstract = True
        ordering = ["-created", "-modified"]


# class TopicMixin(SlugMixin, MetaTagMixin, ImageMixin, TimeStampedModel):
#     name = models.CharField(_("name"), max_length=100, null=False, blank=False)
#     title = models.CharField(_("title"), max_length=255, null=True, blank=True)
#     icon = models.CharField(_("icon"), max_length=100, null=True, blank=True)
#     icon_image = models.ImageField(_("Icon Image"), upload_to=upload_location, null=True, blank=True)
#     content = RichTextUploadingField(_("content"), blank=True, null=True)
#     pipedrive_id = models.PositiveIntegerField(_('Pipedrive ID'), null=True, blank=True)
#     # posts = models.ManyToManyField("blog.Post",blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         abstract = True


class FAQMixin(StatusMixin, TimeStampedModel):
    question = models.CharField(
        _("FAQ Question"), max_length=255, blank=True, null=True
    )
    answer = RichTextUploadingField(_("FAQ Answer"), blank=True, null=True)

    def __str__(self):
        return self.question

    class Meta:
        abstract = True


class TopicMixin(SlugMixin, MetaTagMixin, ImageMixin, TimeStampedModel):
    name = models.CharField(
        _("name"), max_length=100, null=False, blank=False
    )
    title = models.CharField(
        _("title"), max_length=255, null=True, blank=True
    )
    icon = models.CharField(
        _("icon"), max_length=100, null=True, blank=True
    )
    icon_image = models.ImageField(
        _("Icon Image"), upload_to=upload_location, null=True, blank=True
    )
    content = RichTextUploadingField(_("content"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
