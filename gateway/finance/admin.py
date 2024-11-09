from django.contrib import admin
from .models import GateWay, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_paid')
    list_filter = ['is_paid'] 

admin.site.register(GateWay)
admin.site.register(Payment, PaymentAdmin)