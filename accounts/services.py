import re

from django.contrib.auth import user_logged_in
from rest_framework_simplejwt.tokens import RefreshToken


def get_access_token(user, request):
    token = str(RefreshToken.for_user(user).access_token)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def is_valid_phone(phone):
    if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone) is None:
        return False
    return True
