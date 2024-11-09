from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('finance/', include('finance.urls')),
    path('package/', include('package.urls')),
    path('purchase/',include('purchase.urls')),
]
