from rest_framework import serializers


class BaseUserSerializer(serializers.ModelSerializer):
    user_created = serializers.SerializerMethodField()

    def get_user_created(self, obj):
        return self.get_user_info(obj.user)

    def get_user_info(self, user):
        if user:
            return {
                'email': user.email,
                'name': user.name
            }
        return None
