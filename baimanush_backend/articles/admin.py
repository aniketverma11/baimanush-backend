from django.contrib import admin
from baimanush_backend.articles.models import Post, Reference, SubscribeMail, Tag
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.utils.html import format_html


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


# class PostAdmin(ImportExportModelAdmin):
class PostAdmin(admin.ModelAdmin):
    def get_image(self, obj):
        return (
            format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px;" />',
                obj.image.url,
            )
            if obj.image
            else None
        )

    get_image.short_description = "Post Image"

    fieldsets = (
        (
            "Post Details",
            {
                "fields": (
                    "type",
                    "slug",
                    "title",
                    "category",
                    "tags",
                    "minutes_read",
                    "author",
                    "publish",
                )
            },
        ),
        ("Content", {"fields": ("short_description", "content", "audio")}),
        ("Image", {"fields": ("image", "image_description", "get_image")}),
        (
            "Meta Information",
            {"fields": ("meta_title", "meta_description", "meta_keywords")},
        ),
        (
            "Status",
            {
                "fields": (
                    "is_for_members",
                    "home_screen",
                    "is_draft",
                    "is_trending",
                    "is_active",
                    "is_deleted",
                )
            },
        ),
        ("Tracking", {"fields": ("views_count", "created_by", "modified_by")}),
    )

    readonly_fields = ("get_image",)
    resource_class = PostResource
    list_display = (
        "slug",
        "type",
        "get_image",
        "title",
        "category",
        "minutes_read",
        "author",
        "is_for_members",
        "home_screen",
        "is_draft",
        "is_trending",
        "publish",
        "views_count",
        "created",
        "created_by",
    )
    list_filter = (
        "type",
        "slug",
        "category",
        "is_for_members",
        "home_screen",
        "is_draft",
    )
    search_fields = ("slug", "title", "author")
    filter_horizontal = ("sub_categories", "tags")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    model = Reference
    list_display = [
        "slug",
        "title",
        "url",
        "created",
        "modified",
        "is_active",
        "is_deleted",
    ]


@admin.register(SubscribeMail)
class SubscribeMailAdmin(admin.ModelAdmin):
    model = SubscribeMail
    ist_display = ["mail", "created", "modified", "is_active", "is_deleted"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ["slug", "tag", "created", "modified", "is_active", "is_deleted"]
