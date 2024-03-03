from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid','name', 'description', 'created')
    search_fields = ('uuid', 'name', 'description')
    inlines = [SubCategoryInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'category', 'description', 'created')
    list_filter = ('category',)
    search_fields = ('uuid', 'name', 'category__name', 'description', 'created')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
