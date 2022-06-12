from clientapp.models import CustomerGoal
from rest_framework import viewsets, status
from rest_framework.response import Response
from brandapp.models import BrandPlan, BrandPromotion
from modules.pagination import get_paginated_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser, MultiPartParser
from clientapp.serializers import PlanPromotionSerializer, SubscribePlanSerializer, EnrollPlanSerializer
class CustomerViewSet(viewsets.ModelViewSet):
    '''
        Customer ViewSet
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = [JSONParser,MultiPartParser]


    def list(self, request):
        '''
            List all the available plans
        '''
        user = request.user
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=PlanPromotionSerializer,
            queryset=BrandPlan.objects.filter(is_active=True),
            request=request,
            view=self
        )

    def create(self, request):
        '''
            Create a new customer goal
        '''
        serialzer = SubscribePlanSerializer(data = request.data)
        serialzer.is_valid(raise_exception= True)
        data = serialzer.data
        plan = BrandPlan.objects.filter(id = data['plan']).first()
        promotion = BrandPromotion.objects.filter(brand_plan = plan, is_active = True).first()
        if promotion:
            benefit = promotion.benefit_percentage
        elif plan:
            benefit = plan.benefit_percentage
        data.update(
            {
                "plan" : plan.id,
                "user" : request.user.id,
                "customer_name" : request.user.username,   
                "selected_amount": plan.amount_options,
                "selected_tenure":plan.tenure_options,
                "benefit_percentage":benefit,
                "benefit_type":plan.benefit_type,
                "deposit_amount":plan.amount_options

            }
        )
        save_serializer =  EnrollPlanSerializer(data = data)
        save_serializer.is_valid(raise_exception=True)
        save_serializer.save()

        return Response( 
            { "success" : True,
              "message":"User Enrolled to the plan successfully" 
            },
            status= status.HTTP_201_CREATED
        )

