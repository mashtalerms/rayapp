from asyncio import run

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from news.services import NewsParsingService
from rayapp.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from news.models.news import News
from news.serializers.news import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)

    # permission_classes = (IsAdminUserOrReadOnly,)
    search_fields = ('title', 'user__name', 'user__email', 'url',)
    ordering_fields = ('title', 'user__name', 'user__email', 'url',)
    filterset_fields = ('title', 'user__name', 'user__email', 'url',)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def tech_download_news_from_api(self, request):
        async def async_main():
            service = NewsParsingService()
            await service.main()

        run(async_main())
        return Response({"detail": "OK"}, status=200)
