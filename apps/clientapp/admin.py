from django.contrib import admin
from clientapp.models import CustomerGoal
# Register your models here.

class CustomerGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan','created_on', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'user', 'plan', 'customer_name')
    ordering = ['-created_on']

admin.site.register(CustomerGoal, CustomerGoalAdmin)