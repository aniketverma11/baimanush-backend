from django.contrib import admin
from baimanush_backend.articles.models import Post, Reference,SubscribeMail
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource
    list_display = ('slug', 'title', 'category', 'minutes_read', 'author', 'is_for_members', 'home_screen', 'is_draft', 'publish', 'views_count', "created", 'created_by')
    list_filter = ('slug','category', 'is_for_members', 'home_screen', 'is_draft')
    search_fields = ('slug','title', 'author')
    filter_horizontal = ('sub_categories',)


admin.site.register(Post, PostAdmin)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    model = Reference

@admin.register(SubscribeMail)
class SubscribeMailAdmin(admin.ModelAdmin):
	model = SubscribeMail