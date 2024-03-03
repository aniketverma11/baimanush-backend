from django.db import models

from baimanush_backend.utils.behaviours import UUIDMixin, StatusMixin


class Category(UUIDMixin, StatusMixin):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class SubCategory(UUIDMixin, StatusMixin):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Categories"