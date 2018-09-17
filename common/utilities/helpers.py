import phonenumbers

from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python

def format_phone_number_prefix(phone_number):
    assert isinstance(phone_number, (str,))
    return '+{}'.format(phone_number) if not phone_number.startswith('+') \
        else phone_number
        
def validate_phone_number(phone_number):
    error_msg = {
        "phone_number": "Enter a valid phone number."
    }
    phne = format_phone_number_prefix(phone_number)
    phne = to_python(phne)
    if not phonenumbers.is_valid_number(phne):
        raise ValidationError(error_msg)