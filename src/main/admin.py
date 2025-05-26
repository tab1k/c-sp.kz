from django.contrib import admin
from .models import *

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'description', 'category__name')  # добавили поиск по названию категории
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    inlines = [ProductAttributeValueInline]



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']
    search_fields = ('name', 'parent__name')
    ordering = ('name',)
    list_filter = ('parent',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.GET.get('parent__isnull', None):
            return queryset.filter(parent__isnull=True)
        return queryset


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product__name', 'attribute__name', 'value')
    ordering = ('product',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
