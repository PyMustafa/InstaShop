from django.contrib import admin
from .models import Category


# Register your models here.

# admin.site.register(ProductCategory)

@admin.register(Category)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'created_at', 'updated_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
