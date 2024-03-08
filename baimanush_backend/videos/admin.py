from django.contrib import admin

from baimanush_backend.videos.models import Video
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video


class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource


admin.site.register(Video, VideoAdmin)