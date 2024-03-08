from django.contrib import admin
from baimanush_backend.articles.models import Post, Reference,SubscribeMail
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource


admin.site.register(Post, PostAdmin)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    model = Reference

@admin.register(SubscribeMail)
class SubscribeMailAdmin(admin.ModelAdmin):
	model = SubscribeMail