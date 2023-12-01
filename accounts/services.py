import random
import re

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from accounts.models import User


def get_access_token(user, request):
    token = str(RefreshToken.for_user(user).access_token)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def get_user_by_token(token: str):
    access_token_obj = AccessToken(token)
    user_id = access_token_obj['user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = AnonymousUser()
    return user


def generate_password(l: int = 8):
    return ''.join([random.choice('qwertyuiopasdfghjklzxcvbnm1234567890#%$&!') for _ in range(l)])


def is_valid_phone(phone):
    if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone) is None:
        return False
    return True
