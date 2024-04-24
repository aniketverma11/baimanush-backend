from django.db import models
from django.utils.translation import gettext_lazy as _

from baimanush_backend.utils.behaviours import UUIDMixin, StatusMixin, SlugMixin


class Category(SlugMixin, UUIDMixin, StatusMixin):
    name = models.CharField(_("English Name"), max_length=100, blank=True)
    marathi_name = models.CharField(_("Marathi Name"), max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} {self.marathi_name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(SlugMixin, UUIDMixin, StatusMixin):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Categories"
