import re

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.services import get_access_token, is_valid_phone


class Authentication(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    @action(methods=["POST"], detail=False, url_path="auth", permission_classes=[AllowAny])
    def authorization_user(self, request: Request) -> Response:
        """
        Authorizes a user based on the provided email and password.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with the token and user data.
        """
        email: str = request.data.get("email")
        password: str = request.data.get("password")

        try:
            user: User = User.objects.get(email=email)
            if user.check_password(password):
                user_data = self.get_serializer(user).data
                token: str = get_access_token(user, request)
                return Response({'token': token, 'user': user_data}, status=200)
            else:
                raise Exception
        except Exception:
            return Response({'detail': 'Invalid login or password'}, status=403)

    @action(methods=['POST'], detail=False, url_path='registration', permission_classes=[AllowAny])
    def registration(self, request: Request) -> Response:
        """
        Register a new user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with the token and user data.
        """
        email: str = request.data.get('email')
        username: str = request.data.get('username')
        password: str = request.data.get('password')
        repeat_password: str = request.data.get('repeat_password')
        name: str = request.data.get('name')
        phone_number: str = request.data.get('phone_number')

        if not email or not password or not repeat_password or not name or not username or not phone_number:
            resp = {}
            if not email:
                resp['email'] = 'Email required.'
            if not password:
                resp['password'] = 'Password required.'
            if not repeat_password:
                resp['repeat_password'] = 'Password repeat required.'
            if not name:
                resp['name'] = 'Name required.'
            if not username:
                resp['username'] = 'Username required.'
            if not phone_number:
                resp['phone_number'] = 'Phone number required.'
            return Response(resp, status=400)

        if User.objects.filter(email__iexact=email).exists():
            return Response({'email': 'Email already exists'}, status=400)

        if password != repeat_password:
            return Response({'repeat_password': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'username': 'Username already exists'}, status=400)

        if not is_valid_phone(phone_number):
            return Response({'phone_number': 'Invalid phone number'}, status=400)

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
