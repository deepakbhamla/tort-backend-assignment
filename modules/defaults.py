import uuid
from django.core.validators import RegexValidator

def get_default_address():
    '''
        Get default address format for JSONField
    '''
    return {
        'street' : '',
        'city' : '',
        'state' : '',
        'pin_code' : '',
        'country' : ''
    },


def get_logo_upload_path(instance, filename):
    '''
        Get unique logo upload path
        retun: brand_logo/<brand_partner_id>/<uuid>_<filename>
    '''
    return f'brand_logo/{instance.brand_name.replace(" ","_")}/{uuid.uuid4()}_{filename.replace(" ", "_")}'


def get_cover_upload_path(instance, filename):
    '''
        Get unique cover upload path
        return: brand_cover/<brand_partner_id>/<uuid>_<filename>
    '''
    return f'brand_cover/{instance.brand_name.replace(" ","_")}/{uuid.uuid4()}_{filename.replace(" ", "_")}'


def get_promotion_upload_path(instance, filename):
    '''
        Get unique cover upload path
        return: brand_cover/<brand_partner_id>/<uuid>_<filename>
    '''
    return f'brand_promotion/{instance.promotion_name.replace(" ","_")}/{uuid.uuid4()}_{filename.replace(" ", "_")}'


def get_phone_number_format(phone_number):
    '''
        validating phone number format
        return: phone_number

    '''
    return RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
