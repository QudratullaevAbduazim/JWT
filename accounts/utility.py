from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import re

def send_simple_email(user_email, code):
    subject = 'Tasdiqlash kodi'
    message = f'Sizning tasdiqlash kodingiz: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    receipient_list = [user_email]
    
    send_mail(subject, message, from_email, receipient_list)
    return True

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def check_email(email):
    if re.fullmatch(email_regex, email):
        return email
    else:
        raise ValidationError({"success": False, "message": "Email xato kiritilgan"})
