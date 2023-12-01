from rest_framework import serializers

from news.models.news import News


class NewsSerializer(serializers.ModelSerializer):
    user_created = serializers.SerializerMethodField()

    def get_user_created(self, obj):
        if obj.user:
            user_info = {
                'email': obj.user.email,
                'name': obj.user.name
            }
            return user_info

    class Meta:
        model = News
        fields = '__all__'
