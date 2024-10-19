from rest_framework import serializers
from apps.user.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', "avatar_thumbnail", "last_name", "first_name", "phone", "email"]
class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', "avatar_thumbnail"]
