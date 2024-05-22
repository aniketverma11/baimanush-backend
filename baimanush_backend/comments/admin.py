from django.contrib import admin
from .models import PostComments, PhotoComments, VideoComments

class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'post', 'user', 'created')
    search_fields = ('id','content', 'user', 'post__title')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

class PhotoCommentsAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'photo', 'user', 'created')
    search_fields = ('id','content', 'user', 'photo__title')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

class VideoCommentsAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'video', 'user', 'created')
    search_fields = ('id','content', 'user', 'video__title')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(PhotoComments, PhotoCommentsAdmin)
admin.site.register(VideoComments, VideoCommentsAdmin)