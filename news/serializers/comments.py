from news.models.comments import Comment
from news.serializers.base import BaseUserSerializer


class CommentSerializer(BaseUserSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
