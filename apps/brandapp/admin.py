from django.contrib import admin
from brandapp.models import BrandPartner, BrandPlan, BrandPromotion
# Register your models here.

def activate_accounts(modeladmin, request, queryset):
    for query in queryset:
        query.is_active = True
        query.save()


def deactivate_accounts(modeladmin, request, queryset):
    for query in queryset:
        query.is_active = False
        query.save()


activate_accounts.short_description = "Activate accounts"
deactivate_accounts.short_description = "Deactivate accounts"


class BrandPartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'brand_name', 'brand_website', 'brand_email', 'created_on']
    search_fields  = ['id', 'brand_name', 'brand_website', 'brand_email']


class BrandPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan_name', 'brand_partner', 'amount_options', 'tenure_options', 'is_active')
    search_fields  = ('id', 'plan_name', 'brand_partner__brand_name')
    list_per_page = 50
    actions = (activate_accounts,deactivate_accounts)

    def get_active(self, obj):
        return obj.is_active

    get_active.short_description = 'Active'

    def get_queryset(self, request):
        qs = super(BrandPlanAdmin, self).get_queryset(request)
        return qs


class BrandPromotionAdmin(admin.ModelAdmin):
    list_display= ('id', 'promotion_name', 'brand_plan', 'is_active' )
    search_fields =  ('id', 'promotion_name', 'brand_plan__plan_name')
    readonly_fields = ('reach_counts',)
    list_per_page = 50
    actions = (activate_accounts,deactivate_accounts)

    def get_active(self, obj):
        return obj.is_active

    get_active.short_description = 'Active'

    def get_queryset(self, request):
        qs = super(BrandPromotionAdmin, self).get_queryset(request)
        return qs


admin.site.register(BrandPartner, BrandPartnerAdmin)
admin.site.register(BrandPlan, BrandPlanAdmin)
admin.site.register(BrandPromotion, BrandPromotionAdmin)