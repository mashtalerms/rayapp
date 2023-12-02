from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.services import is_valid_phone


class Profile(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=["GET"], detail=False)
    def info(self, request: Request) -> Response:
        """
        Get information about the user.
        Args:
            request (Request): The request object.
        Returns:
            Response: The serialized user data.
        """
        serializer = self.get_serializer(request.user, many=False)
        serialized_data = serializer.data
        return Response(serialized_data)

    @transaction.atomic
    @action(methods=["PUT"], detail=False)
    def change_profile(self, request: Request) -> Response:
        """
        Updates the user's profile with the provided data.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with a success message.
        """
        user = request.user
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")

        if name is not None and user.name != name:
            user.name = name
        if email is not None and user.email != email:
            user.email = email
        if phone_number is not None and user.phone_number != phone_number and is_valid_phone(phone_number):
            user.phone_number = phone_number

        user.save()
        return Response({"detail": "User data has been updated"}, status=200)

    @transaction.atomic
    @action(methods=["PUT"], detail=False)
    def change_password(self, request: Request) -> Response:
        """
        Change the user's password.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        new_password: str = request.data.get("new_password")
        user: User = request.user

        if not new_password:
            return Response({"detail": "New password is required"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been changed"}, status=200)
