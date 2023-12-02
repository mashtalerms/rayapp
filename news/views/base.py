from collections import OrderedDict

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

import json


class CacheMixin:
    """
    Mixin to handle caching logic.
    """
    cache_timeout = 0

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            cache_key = f"{request.path}?{request.GET.urlencode()}"
            cached_data = cache.get(cache_key)

            if cached_data is not None:
                try:
                    cached_data = json.loads(cached_data, object_pairs_hook=OrderedDict)
                except json.JSONDecodeError:
                    pass

                response = Response(cached_data)
                response.accepted_renderer = self.get_renderers()[0]
                response.accepted_media_type = self.get_renderers()[0].media_type
                response.renderer_context = self.get_renderer_context()
                return response

        response = super().dispatch(request, *args, **kwargs)

        if request.method == "GET" and response.status_code == 200:
            cache_key = f"{request.path}?{request.GET.urlencode()}"
            serialized_data = json.dumps(response.data, cls=DjangoJSONEncoder)

            cache.add(cache_key, serialized_data, self.cache_timeout)

        return response


class UserActionMixin:
    """
    Mixin to handle user actions like create and destroy.
    """

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Set the user ID in the request data and call the parent create method.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.
        """
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs):
        """
        Destroys an instance.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response indicating the success or failure of the operation.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
