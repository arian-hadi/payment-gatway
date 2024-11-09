from django.contrib import admin
from .models import Package, PackageAttribute
from django.contrib.admin import register


class PackageAttributeInline(admin.TabularInline):
    model = PackageAttribute

@register(Package)
class PackageModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    inlines = [PackageAttributeInline]

