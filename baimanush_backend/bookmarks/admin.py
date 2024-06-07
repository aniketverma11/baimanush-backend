from django.contrib import admin
from .models import BookMarks

class BookMarksAdmin(admin.ModelAdmin):
    list_display = ("id",'created_by', 'is_active', 'created')
    search_fields = ("id",'created_by__email',)
    filter_horizontal = ('articles', 'videos', 'photos')


admin.site.register(BookMarks, BookMarksAdmin)
