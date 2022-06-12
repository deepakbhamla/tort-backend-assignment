from django.db import models
from brandapp.models import BrandPlan
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from modules.choices import BENEFIT_CHOICES, AMOUNT_CHOICES, TENURE_CHOICES
# Create your models here.

class CustomerGoal(models.Model):
    '''
        Customer Goal Model
    '''
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING, related_name='customer_goals')
    plan = models.ForeignKey(BrandPlan, on_delete= models.DO_NOTHING, related_name='customer_goals')
    customer_name = models.CharField(max_length=100, help_text='required')
    selected_amount = models.IntegerField(choices=AMOUNT_CHOICES, default=1)
    selected_tenure = models.IntegerField(choices=TENURE_CHOICES, default=1)
    benefit_type = models.IntegerField(choices=BENEFIT_CHOICES, default=1)
    benefit_percentage = models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
    start_date = models.DateField(auto_now_add=False, blank=True, null=True)
    deposit_amount = models.IntegerField(default=0, validators=[MaxValueValidator(1000000),MinValueValidator(0)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}. {self.customer_name}'

    def get_amount_options_display(self):
        return self.get_amount_options_display()
    
    class Meta:
        db_table = 'clientapp_customer_goals'
        app_label = 'clientapp'
        verbose_name = 'Customer Goal'
        verbose_name_plural = 'Customer Goals'
        ordering = ['-created_on']

