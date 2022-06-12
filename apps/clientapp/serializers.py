from rest_framework import serializers
from brandapp.models import BrandPlan
from clientapp.models import CustomerGoal
from modules.constants import AMOUNT_TYPE, TENURE_TYPE, BENEFIT_TYPE, PROMOTION_TYPE
from modules.choices import AMOUNT_CHOICES, TENURE_CHOICES, BENEFIT_CHOICES, PROMOTION_CHOICES


class PlanPromotionSerializer(serializers.ModelSerializer):
    """
        get all plans with promotions benefit percentage
    """
    amount_options = serializers.SerializerMethodField()
    tenure_options = serializers.SerializerMethodField()
    benefit_type = serializers.SerializerMethodField()

    class Meta:
        model = BrandPlan
        fields = ('id', 'plan_name', 'plan_description', 'amount_options', 'tenure_options', 'benefit_type', 'benefit_percentage')
        read_only_fields = fields

    def get_amount_options(self, obj):
        return obj.get_amount_options_display()

    def get_tenure_options(self, obj):
        return obj.get_tenure_options_display()

    def get_benefit_type(self, obj):
        return obj.get_benefit_type_display()
        

class SubscribePlanSerializer(serializers.ModelSerializer):
    """
        subscribe to a plan
    """
    class Meta:
        model = CustomerGoal
        fields = '__all__'


    def validate(self, attrs):
        """
            Validate the request data
        """
        plan = attrs.get('plan__id')
        user = attrs.get('user')
        if BrandPlan.objects.filter(id = plan).exists():
            raise serializers.ValidationError("Plan does not exist...")
        if CustomerGoal.objects.filter(user = user, plan = plan).exists():
            raise serializers.ValidationError("Already Enrolled...")    
        return super().validate(attrs)


class  EnrollPlanSerializer(serializers.ModelSerializer):
    """
        enroll to a plan
    """
    class Meta:
        model = CustomerGoal
        fields = ('id', 'user', 'plan', 'customer_name', 'selected_amount', 'selected_tenure', 'benefit_type', 'benefit_percentage')

    def validate(self, attrs):
        return super().validate(attrs)