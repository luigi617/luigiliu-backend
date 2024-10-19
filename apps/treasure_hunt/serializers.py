from rest_framework import serializers
from apps.treasure_hunt.models import GroupTreasure, Treasure, TreasureHint, Group, TreasureHuntGame
from apps.user.models import User
from apps.user.serializers import BasicUserSerializer
from config.settings.base import MEDIA_URL

class GroupSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ["id", "name", "users"]
    
    def get_users(self, obj):
        users = User.objects.filter(pk__in = obj.users)
        data = BasicUserSerializer(users, many = True).data
        return data

class GroupTreasureListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GroupTreasure
        fields = ["treasure", "status"]

class TreasureHuntGameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TreasureHuntGame
        fields = ["id", "time_started", "time_ended", "is_started", "groups", "treasures"]

class GroupTreasureHuntGameSerializer(serializers.Serializer):
    game = TreasureHuntGameSerializer()
    treasures = GroupTreasureListSerializer(many=True)
    group = GroupSerializer()

class TreasureHuntGameListSerializer(serializers.Serializer):
    game = TreasureHuntGameSerializer()
    groups = GroupSerializer(many=True)



class TreasureRetrieveSerializer(serializers.Serializer):
    object = serializers.SerializerMethodField()
    status = serializers.IntegerField()
    def get_object(self, obj):
        return MEDIA_URL + obj["object"]

class GroupTreasureHintListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hint_img = serializers.CharField()
    hint = serializers.CharField()
    requirement_for_hint = serializers.CharField()
    status = serializers.IntegerField()
    
class TreasureHintListSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = TreasureHint
        fields = ["id", "hint_img", "hint", "requirement_for_hint"]

class TreasureWithHintSerializer(serializers.ModelSerializer):
    hints = TreasureHintListSerializer(many=True)
    class Meta:
        model = Treasure
        fields = ["id", "object", "hints"]



class TreasureHuntGameTreasureHintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasureHint
        fields = ["hint_img", "hint", "requirement_for_hint"]
class TreasureHuntGameTreasureListSerializer(serializers.ModelSerializer):
    hints = TreasureHuntGameTreasureHintListSerializer(many=True)
    class Meta:
        model = Treasure
        fields = ["object", "hints"]

class TreasureHuntGameRetrieveSerializer(serializers.Serializer):
    game = TreasureHuntGameSerializer()
    groups = GroupSerializer(many=True)
    treasures = TreasureHuntGameTreasureListSerializer(many=True)

class GroupTreasureProcessSerializer(serializers.Serializer):
    group = GroupSerializer()
    number_completed_treasures = serializers.IntegerField()
    number_treasures = serializers.IntegerField()
   
class TreasureEvidenceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    object = serializers.SerializerMethodField()
    evidence = serializers.SerializerMethodField()
    date_modified = serializers.CharField()
    status = serializers.IntegerField()
    type = serializers.CharField()

    def get_evidence(self, obj):
        return MEDIA_URL + obj["evidence"]
    def get_object(self, obj):
        if "treasure_hunt/treasure" in obj["object"]:
            return MEDIA_URL + obj["object"]
        return obj["object"]
   
