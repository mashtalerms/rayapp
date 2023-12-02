from rest_framework import serializers

from news.models.news import News
from news.serializers.base import BaseUserSerializer
from news.serializers.comments import CommentSerializer


class NewsSerializer(BaseUserSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data

    class Meta:
        model = News
        fields = '__all__'
