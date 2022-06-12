from django.urls import path

from rest_framework.routers import DefaultRouter
from clientapp.views import CustomerViewSet

router = DefaultRouter()
router.register('', CustomerViewSet, basename='plans')

urlpatterns = [
    path('v1/plans/', CustomerViewSet.as_view({'get' : 'list', 'post' : 'create'}), name='plan-list'),
]
