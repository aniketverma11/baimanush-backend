from django.contrib import admin

from baimanush_backend.videos.models import Video
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    resource_class = VideoResource
    list_display = (
        "slug",
        "title",
        "short_description",
        "publish",
        "category",
        "minutes_read",
        "author",
        "home_screen",
        "is_for_members",
        "is_draft",
        "is_trending",
        "publish",
        "created",
        "created_by",
    )
    list_filter = ("slug", "category", "is_for_members", "is_draft")
    search_fields = ("slug", "title", "author")
    filter_horizontal = ("sub_categories", "tags")


admin.site.register(Video, VideoAdmin)
