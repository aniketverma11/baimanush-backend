from django.contrib import admin
from django.contrib import admin

from baimanush_backend.photos.models import Photos, Images
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ImageInline(admin.TabularInline):
    model = Images
    extra = 3  

class PhotosResource(resources.ModelResource):
    class Meta:
        model = Photos


class PhotosAdmin(ImportExportModelAdmin):
    inlines = [ImageInline]
    resource_class = PhotosResource
    list_display = ('slug','title', 'short_description', 'publish', 'category', 'minutes_read', 'author', 'is_for_members',"home_screen", 'is_draft' ,'publish', "created", 'created_by')
    list_filter = ('slug','category', 'is_for_members', 'is_draft')
    search_fields = ('slug','title', 'author')
    filter_horizontal = ('sub_categories', 'tags')


admin.site.register(Photos, PhotosAdmin)
admin.site.register(Images)