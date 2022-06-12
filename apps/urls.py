from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('partner/', include('apps.brandapp.urls')),
    path('customer/', include('apps.clientapp.urls')),
]
