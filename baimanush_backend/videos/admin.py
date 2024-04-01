from django.contrib import admin

from baimanush_backend.videos.models import Video
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.utils.html import format_html


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video


class VideoAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return format_html('<img src="{}" style="max-height: 300px; max-width: 300px;" />', obj.image.url) if obj.image else None

    
    get_image.short_description = 'Video Thumbnail Image'

    fieldsets = (
        ('Post Details', {
            'fields': ('type','slug', 'title', 'category','tags', 'minutes_read', 'author', 'publish')
        }),
        ('Content', {
            'fields': ('video', 'short_description', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_description', "get_image")
        }),
        ('Status', {
            'fields': ('is_for_members', 'home_screen', 'is_draft', 'is_trending', 'is_active', 'is_deleted')
        }),
        ('Tracking', {
            'fields': ('views_count', 'created_by', 'modified_by')
        }),
    )
    readonly_fields = ('get_image',)
    resource_class = VideoResource
    list_display = (
        "slug",
        "type",
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
    list_filter = ('type',"slug", "category", "is_for_members", "is_draft")
    search_fields = ("slug", "title", "author")
    filter_horizontal = ("tags",)


admin.site.register(Video, VideoAdmin)
