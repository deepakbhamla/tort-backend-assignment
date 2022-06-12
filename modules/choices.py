from django.utils.translation import gettext_lazy as _

US9 = ONE_MONTH = CASHBACK = BY_USER = 1
US15 = THREE_MONTHS = EXTRA_CASHBACK = BY_TIME = 2
US19 = SIX_MONTHS = WALLET_POINT = 3
US25 = TWELVE_MONTH = 4
US49 = EIGHTEEN_MONTHS = 5
US75 = TWENTYFOUR_MONTH = 6

BENEFIT_CHOICES = (
    (CASHBACK, _("CASHBACK")),
    (EXTRA_CASHBACK, _("EXTRA_CASHBACK")),
    (WALLET_POINT, _("WALLET_POINT")),
)

AMOUNT_CHOICES = (
    (US9, _("US$09.99")),
    (US15, _("US$15.49")),
    (US19, _("US$19.99")),
    (US25, _("US$25.49")),
    (US49, _("US$49.49")),
    (US75, _("US$75.99")),

)

TENURE_CHOICES = (
    (ONE_MONTH, _("1 MONTH")),
    (THREE_MONTHS, _("3 MONTHS")),
    (SIX_MONTHS, _("6 MONTHS")),
    (TWELVE_MONTH, _("12 MONTHS")),
    (EIGHTEEN_MONTHS, _("18 MONTHS")),
    (TWENTYFOUR_MONTH, _("24 MONTHS")),

)

PROMOTION_CHOICES = (
    (BY_USER, _("BY NUMBER OF USER")),
    (BY_TIME, _("BY TIME PERIOD")), 
)