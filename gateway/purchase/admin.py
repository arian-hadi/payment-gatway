from django.contrib.admin import register
from django.contrib import admin
from purchase.models import Purchase
# Register your models here.
@register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'price', 'status']
    list_filter = ['status']