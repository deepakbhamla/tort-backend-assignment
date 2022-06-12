from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from modules.pagination import get_paginated_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser, MultiPartParser
from brandapp.models import BrandPartner, BrandPlan, BrandPromotion
from brandapp.serializers import PlanReadOnlySerializer, PlanDetailsSerializer, PlanCreateSerializer, PromotionReadOnlySerializer, PromotionDetailSerializer, PromotionCreateSerializer

# Create your views here.

class PlanViewSet(viewsets.GenericViewSet):
    """
        viewset  for listing/ retrieving and creating brand plan details
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = BrandPlan.objects.all()
    parser_classes = [JSONParser,MultiPartParser]


    def list(self, request):
        '''
            List all the active plans
        '''
        user = request.user
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PlanReadOnlySerializer,
            queryset=self.queryset.filter(is_active=True),
            request=request,
            view=self
        )

    def retrieve(self, request, plan_id):
        '''
            Retrieve a plan details by plan_id
        '''
        user = request.user
        qs = get_object_or_404(BrandPlan, pk=plan_id)
        serializer = PlanDetailsSerializer(qs)
        data = serializer.data
        return Response(data ,status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = PlanCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {
                'success':True,
                'message':f"new plan added : {request.data.get('plan_name')}",
                'plan_name' : request.data.get('plan_name'),
                'id' : serializer.data.get('id')

            },
            status= status.HTTP_201_CREATED
        )


class PromotionViewSet(viewsets.GenericViewSet):
    """
        viewset  for listing/ retrieving and creating brand plan details
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = BrandPromotion.objects.all()
    parser_classes = [JSONParser,MultiPartParser]


    def list(self, request, plan_id):
        '''
            list all promotions for a plan
        '''
        user = request.user
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PromotionReadOnlySerializer,
            queryset=self.queryset.filter(is_active=True, brand_plan = plan_id),
            request=request,
            view=self
        )

    def retrieve(self, request, promotion_id):
        '''
            retrieve a promotion by promotion_id
        '''
        user = request.user
        qs = get_object_or_404(BrandPromotion, pk=promotion_id)
        serializer = PromotionDetailSerializer(qs)
        data = serializer.data
        return Response(data ,status=status.HTTP_200_OK)

    def create(self, request, plan_id):
        '''
            create a promotion
        '''
        data = request.data
        serializer = PromotionCreateSerializer(data=data, context={'plan_id': plan_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {
                'success':True,
                'message':f"new promotion added : {request.data.get('promotion_name')}",
                'plan_name' : request.data.get('promotion_name'),
                'id' : serializer.data.get('id')

            },
            status= status.HTTP_201_CREATED
        )
