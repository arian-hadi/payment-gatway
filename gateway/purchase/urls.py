from django.urls import path
from .views import CreatePurchaseView

urlpatterns = [
    path("create/<int:package_id>/",CreatePurchaseView.as_view(), name = "purchase-create"),
]
