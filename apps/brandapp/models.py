from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from modules.choices import BENEFIT_CHOICES, AMOUNT_CHOICES, TENURE_CHOICES, PROMOTION_CHOICES
from modules.defaults import get_default_address, get_logo_upload_path, get_cover_upload_path, get_phone_number_format, get_promotion_upload_path
# Create your models here.


class BrandPartner(models.Model):
    '''
        Brand Partner Model
        
    ''' 
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100, help_text='required')
    brand_description = models.TextField(null=True, blank=True, help_text='optional')
    brand_website = models.URLField(null=True, blank=True,help_text='optional')
    brand_email = models.EmailField(null=True, blank=True,help_text='optional')
    brand_cover = models.ImageField(upload_to=get_cover_upload_path, blank=True, null=True, help_text='optional')
    brand_logo = models.ImageField(upload_to=get_logo_upload_path, blank=True, null=True, help_text='optional')
    brand_phone = models.CharField(validators=[get_phone_number_format], max_length=17, blank=True, unique=True, null=True, help_text='optional')
    brand_address = models.JSONField(default = get_default_address)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}.{self.brand_name}'

    class Meta:
        db_table = 'brandapp_brand_partner'
        app_label = 'brandapp'
        verbose_name = 'Brand Partner'
        verbose_name_plural = 'Brand Partners'
        ordering = ['-id']


class BrandPlan(models.Model):
    '''
        Brand Plan Model

    '''

    brand_partner = models.ForeignKey(BrandPartner, on_delete=models.CASCADE, related_name='brand_plans')
    plan_name = models.CharField(max_length=100, help_text='required')
    plan_description = models.TextField(null=True, blank=True, help_text='optional')
    amount_options = models.IntegerField(choices=AMOUNT_CHOICES, default=1)
    tenure_options = models.IntegerField(choices=TENURE_CHOICES, default=1)
    benefit_type = models.IntegerField(choices=BENEFIT_CHOICES, default=1)
    benefit_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}.{self.plan_name}'

    class Meta:
        db_table = 'brandapp_brand_plan'
        app_label = 'brandapp'
        verbose_name = 'Brand Plan'
        verbose_name_plural = 'Brand Plans'
        ordering = ['id']


class BrandPromotion(models.Model):
    '''
        Brand Promotion Model
        
    ''' 
    brand_partner = models.ForeignKey(BrandPartner, on_delete=models.CASCADE, related_name='brand_promotions')
    brand_plan = models.ForeignKey(BrandPlan, on_delete=models.CASCADE, related_name='brand_promotions')
    promotion_name = models.CharField(max_length=100, help_text='required')
    promotion_description = models.TextField(null=True, blank=True, help_text='optional')
    promotion_image = models.ImageField(upload_to=get_promotion_upload_path, blank=True, null=True, help_text="optional")
    promotion_type = models.IntegerField(choices=PROMOTION_CHOICES, default=1)
    benefit_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
    valid_from = models.DateField('Promotion Valid From',null=True, blank=True)
    valid_to = models.DateField('Promotion Valid To', null=True, blank=True)
    number_of_users = models.IntegerField('Number Of Users To Get The Promotion',blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reach_counts = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.id}.{self.promotion_name}'

    class Meta:
        db_table = 'brandapp_brand_promotion'
        app_label = 'brandapp'
        verbose_name = 'Brand Promotion'
        verbose_name_plural = 'Brand Promotions'
        ordering = ['-id']

    def clean(self):
        super(BrandPromotion, self).clean()
        if self.is_active:
            if self.promotion_type == 1:
                if self.number_of_users <= self.reach_counts:
                    raise ValidationError("This Promotion Exceeds The Number Of Users To Get The Promotion")
            elif self.promotion_type == 2:
                if self.valid_to < datetime.now():
                    raise ValidationError("This Promotion Is Expired")
    


