from django.urls import path
from rest_framework.routers import DefaultRouter
from brandapp.views import PlanViewSet, PromotionViewSet

router = DefaultRouter()
router.register('', PlanViewSet, basename='plans')
router.register('', PromotionViewSet, basename='plans')

urlpatterns = [
    path('v1/plans/', PlanViewSet.as_view({'get' : 'list', 'post' : 'create'}), name='plan-list'),
    path('v1/plan/<str:plan_id>/', PlanViewSet.as_view({'get' : 'retrieve'}), name='plan-detail'),
    path('v1/promotions/<str:plan_id>/', PromotionViewSet.as_view({'get' : 'list', 'post' : 'create'}), name='promotion-list'),
    path('v1/promotion/<str:promotion_id>/', PromotionViewSet.as_view({'get' : 'retrieve'}), name='promotion-details'),
]

urlpatterns += router.urls

