from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.services import is_valid_phone


class Profile(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["GET"], detail=False)
    def info(self, request):
        return Response(self.get_serializer(request.user, many=False).data)

    @transaction.atomic
    @action(methods=["PUT"], detail=False)
    def change_profile(self, request):
        user = request.user
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")

        if user.name != name and name != None:
            user.name = name
        if user.email != email and email != None:
            user.email = email
        if user.phone_number != phone_number and phone_number != None and is_valid_phone(phone_number):
            user.phone_number = phone_number
        user.save()
        return Response({"detail": "Данные пользователя изменены"}, 200)

    @transaction.atomic
    @action(methods=["PUT"], detail=False)
    def change_password(self, request):
        new_password = request.data.get("new_password")
        user = request.user
        if not new_password:
            return Response({"detail": "Укажите новый пароль"}, 400)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Пароль успешно изменен на новый"}, 200)
