from news.models.news import News
from news.serializers.base import BaseUserSerializer


class NewsSerializer(BaseUserSerializer):
    class Meta:
        model = News
        fields = '__all__'
