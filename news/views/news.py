from asyncio import run

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from news.services import NewsParsingService
from news.views.base import CacheMixin, UserActionMixin
from rayapp.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from news.models.news import News
from news.serializers.news import NewsSerializer


class NewsViewSet(CacheMixin, UserActionMixin, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)

    search_fields = ('title', 'user__name', 'user__email', 'url',)
    ordering_fields = ('title', 'user__name', 'user__email', 'url', 'publication_time')
    filterset_fields = ('title', 'user__name', 'user__email', 'url',)

    @action(methods=["POST"], detail=False)
    def tech_download_news_from_api(self, request) -> Response:
        """
            Asynchronously executes the main function.
            Returns:
                Response: The response indicating the success of the operation.
            """

        async def async_main():
            service = NewsParsingService()
            await service.main()

        run(async_main())
        return Response({"detail": "News has been downloaded"}, status=200)
