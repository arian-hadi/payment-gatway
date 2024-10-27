from django.contrib import admin
from .models import Package
from django.contrib.admin import register

@register(Package)
class PackageModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']