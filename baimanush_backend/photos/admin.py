from django.contrib import admin
from django.contrib import admin

from baimanush_backend.photos.models import Photos, Photos_Images
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html

class ImageInline(admin.TabularInline):
    model = Photos_Images
    extra = 3


class PhotosResource(resources.ModelResource):
    class Meta:
        model = Photos


class PhotosAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return format_html('<img src="{}" style="max-height: 500px; max-width: 500px;" />', obj.image.url) if obj.image else None

    
    get_image.short_description = 'Photos Thumbnail'

    fieldsets = (
        ('Post Details', {
            'fields': ('slug', 'title', 'category', 'minutes_read', 'author', 'publish')
        }),
        ('Content', {
            'fields': ('short_description', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_alt', "get_image")
        }),
        ('Status', {
            'fields': ('is_for_members', 'home_screen', 'is_draft', 'is_trending', 'is_active', 'is_deleted')
        }),
        ('Tracking', {
            'fields': ('views_count', 'created_by', 'modified_by')
        }),
    )
    readonly_fields = ('get_image',)
    inlines = [ImageInline]
    resource_class = PhotosResource
    list_display = (
        "slug",
        "title",
        "short_description",
        "publish",
        "category",
        "minutes_read",
        "author",
        "is_for_members",
        "home_screen",
        "is_draft",
        "publish",
        "is_trending",
        "created",
        "created_by",
    )
    list_filter = ("slug", "category", "is_for_members", "is_draft")
    search_fields = ("slug", "title", "author")
    filter_horizontal = ("sub_categories", "tags")


class ImageAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return format_html('<img src="{}" style="max-height: 500px; max-width: 500px;" />', obj.image.url) if obj.image else None

    get_image.short_description = 'Photos Image'
    readonly_fields = ('get_image',)
    list_display = (
        "id",
        "get_image",
        "photo",
        "created"
    )

admin.site.register(Photos, PhotosAdmin)
admin.site.register(Photos_Images, ImageAdmin)
