from rest_framework import serializers
from apps.map.models import Marker
from apps.user.models import User
from apps.user.serializers import BasicUserSerializer
from config.settings.base import MEDIA_URL

class MarkerListSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    # company_image = serializers.SerializerMethodField()
    class Meta:
        model = Marker
        fields = ["id", "lon", "lat", "company_image", "company_name", "address", "phone_number", "tags", "opening_hours", "created_by"]
    
    def get_created_by(self, obj):
        created_by = User.objects.get(pk = obj.created_by.id)
        data = BasicUserSerializer(created_by).data
        return data

    
class MarkerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ["lon", "lat", "company_image", "company_name", "address", "phone_number", "tags", "opening_hours", "created_by"]
