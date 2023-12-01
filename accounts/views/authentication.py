import re

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.services import get_access_token, is_valid_phone


class Authentication(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    @action(methods=["POST"], detail=False, url_path="auth", permission_classes=[AllowAny])
    def authorization_user(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user_data = self.get_serializer(user).data
                token = get_access_token(user, request)
                return Response({'token': token, 'user': user_data}, 200)
            else:
                raise Exception
        except Exception:
            return Response({'detail': 'Неверный логин или пароль'}, 403)

    @action(methods=['POST'], detail=False, url_path='registration', permission_classes=[AllowAny])
    def registration(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        repeat_password = request.data.get('repeat_password')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')

        if not email or not password or not repeat_password or not name or not username or not phone_number:
            resp = {}
            if not email:
                resp['email'] = 'Укажите Email.'
            if not password:
                resp['password'] = 'Укажите пароль.'
            if not repeat_password:
                resp['repeat_password'] = 'Подтвердите пароль.'
            if not name:
                resp['first_name'] = 'Укажите имя.'
            if not username:
                resp['username'] = 'Укажите логин.'
            if not phone_number:
                resp['phone_number'] = 'Укажите номер телефона.'
            return Response(resp, status=400)

        if User.objects.filter(email__iexact=email).exists():
            return Response({'email': 'Данный Email уже зарегистрирован в системе.'}, status=400)

        if password != repeat_password:
            return Response({'repeat_password': 'Пароли не совпадают.'}, status=400)

        if User.objects.filter(email__iexact=email).exists():
            return Response({'email': 'Данный Email уже зарегистрирован в системе.'})

        if User.objects.filter(username=username).exists():
            return Response({'username': 'Данный логин уже зарегистрирован в системе.'})

        if not is_valid_phone(phone_number):
            return Response({'phone_number': 'Неверный номер телефона.'}, status=400)

        user = User(
            name=name,
            email=email,
            username=username,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()

        user_data = self.get_serializer(user).data
        token = get_access_token(user, request)
        return Response({'token': token, 'user': user_data}, 200)
