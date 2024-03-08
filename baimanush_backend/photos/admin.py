from django.contrib import admin
from django.contrib import admin

from baimanush_backend.photos.models import Photos, Images
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ImageInline(admin.TabularInline):
    model = Images
    extra = 3  #
class PhotosResource(resources.ModelResource):
    class Meta:
        model = Photos


class PhotosAdmin(ImportExportModelAdmin):
    inlines = [ImageInline]
    resource_class = PhotosResource


admin.site.register(Photos, PhotosAdmin)