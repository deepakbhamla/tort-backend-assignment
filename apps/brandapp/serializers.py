from rest_framework import serializers
from brandapp.models import BrandPlan, BrandPromotion, BrandPartner
from modules.constants import AMOUNT_TYPE, TENURE_TYPE, BENEFIT_TYPE, PROMOTION_TYPE
from modules.choices import AMOUNT_CHOICES, TENURE_CHOICES, BENEFIT_CHOICES, PROMOTION_CHOICES


class PlanReadOnlySerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    amount_options = serializers.SerializerMethodField()
    tenure_options = serializers.SerializerMethodField()
    benefit_type = serializers.SerializerMethodField()

    class Meta:
        model = BrandPlan
        fields = ('id', 'plan_name', 'plan_description', 'amount_options', 'tenure_options', 'benefit_type', 'benefit_percentage')

    def get_amount_options(self, obj):
        return obj.get_amount_options_display()

    def get_tenure_options(self, obj):
        return obj.get_tenure_options_display()

    def get_benefit_type(self, obj):
        return obj.get_benefit_type_display()


class PlanDetailsSerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
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


class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandPlan
        exclude = ['created_on', 'updated_on',]

    def validate(self, attrs):
        """
            Validate the request data

        """
        amount_options = attrs['amount_options']
        tenure_options = attrs['tenure_options']
        benefit_type = attrs['benefit_type']
        
        if amount_options not in list(AMOUNT_TYPE.keys()):
            raise serializers.ValidationError({
                "amount_options": f'{amount_options} is not a valid choice.',
                "valid_choice" : AMOUNT_CHOICES
            }) 
        if tenure_options not in list(TENURE_TYPE.keys()):
            raise serializers.ValidationError({
                "tenure_options": f'{tenure_options} is not a valid choice.',
                "valid_choice" : TENURE_CHOICES
            })
        if benefit_type not in list(BENEFIT_TYPE.keys()):
            raise serializers.ValidationError({
                "benefit_type": f'{benefit_type} is not a valid choice.',
                "valid_choice" : BENEFIT_CHOICES
            })
        return super().validate(attrs)
 

class PromotionReadOnlySerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    promotion_type = serializers.SerializerMethodField()

    class Meta:
        model = BrandPromotion
        fields = ('id', 'promotion_name', 'promotion_description', 'promotion_image', 'promotion_type', 'brand_plan', 'brand_partner')

    def to_representation(self, instance):
        rep = super(PromotionReadOnlySerializer, self).to_representation(instance)
        rep['brand_plan'] = instance.brand_plan.plan_name
        rep['brand_partner'] = instance.brand_partner.brand_name
        return rep

    def get_promotion_type(self, obj):
        return obj.get_promotion_type_display()


class PromotionDetailSerializer(serializers.ModelSerializer):
    """
        Read only Serializer class for BrandPlan Model
    """
    promotion_type = serializers.SerializerMethodField()

    class Meta:
        model = BrandPromotion
        fields = ('id', 'promotion_name', 'promotion_description', 'promotion_image', 'promotion_type', 'brand_plan', 'brand_partner')

    def to_representation(self, instance):
        rep = super(PromotionDetailSerializer, self).to_representation(instance)
        rep['brand_plan'] = instance.brand_plan.plan_name
        rep['brand_partner'] = instance.brand_partner.brand_name
        return rep

    def get_promotion_type(self, obj):
        return obj.get_promotion_type_display()


class PromotionCreateSerializer(serializers.ModelSerializer):
    brand_plan = serializers.PrimaryKeyRelatedField(queryset=BrandPlan.objects.all(), required=False)
    brand_partner = serializers.PrimaryKeyRelatedField(queryset=BrandPartner.objects.all(), required=False)
    class Meta:
        model = BrandPromotion
        exclude = ['created_on', 'updated_on']

    def validate(self, attrs):
        """
            Validate the request data

        """
        promotion_type = attrs.get('promotion_type', None)
        
        if promotion_type not in list(PROMOTION_TYPE.keys()):
            raise serializers.ValidationError({
                "promotion_options": f'{promotion_type} is not a valid choice.',
                "valid_choice" : PROMOTION_CHOICES
            }) 
        return super().validate(attrs)
 

    def create(self, validated_data):
        plan_id = self.context['plan_id']
        brand_plan = self.get_plan(plan_id)
        brand_partner = brand_plan.brand_partner
        validated_data['brand_plan'] = brand_plan
        validated_data['brand_partner'] = brand_partner
        return super(PromotionCreateSerializer, self).create(validated_data)
        
   
    def get_plan(self, plan_id):
        return BrandPlan.objects.get(id=plan_id)
        
