from django.urls import path
from .views import PricingView
from django.views.generic import TemplateView

urlpatterns = [
    path('pricing/', PricingView.as_view(), name = 'Price view'),
]