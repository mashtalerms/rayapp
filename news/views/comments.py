from rest_framework import viewsets

from news.models import Comment
from news.serializers.comments import CommentSerializer
from news.views.base import CacheMixin, UserActionMixin
from rayapp.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class CommentsViewSet(CacheMixin, UserActionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)

    search_fields = ('text', 'user__name', 'user__email', 'news__title', 'news__url', 'news__source',)
    ordering_fields = (
        'text', 'user__name', 'user__email', 'news__title', 'news__url', 'news__source', 'publication_time')
    filterset_fields = ('text', 'user__name', 'user__email', 'news__title', 'news__url', 'news__source',)
