
# serializers.py

from rest_framework import serializers
from .models import StandingTeam, Game, Team, GameStatus

class StandingTeamSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='team.id')
    team_name = serializers.CharField(source='team.name')
    team_logo = serializers.CharField(source='team.logo')
    home = serializers.CharField(source='home_wins_losses')
    away = serializers.CharField(source='away_wins_losses')
    ll10 = serializers.CharField(source='last10_wins_losses')

    class Meta:
        model = StandingTeam
        fields = [
            'team_id',
            'team_name',
            'team_logo',
            'rank',
            'pct',
            'wins',
            'losses',
            'home',
            'away',
            'll10'
        ]


class TeamInfoSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='id')
    team_full_name = serializers.CharField(source='full_name')
    team_abbr_name = serializers.CharField(source='abbr_name')
    logo = serializers.CharField(source='logo')
    team_name = serializers.CharField(source='name')
    team_wins_losses = serializers.CharField()
    qtr_points = serializers.ListField(
        child=serializers.IntegerField(),
        default=[]
    )
    point = serializers.IntegerField()

    class Meta:
        model = Team
        fields = [
            'team_id',
            'team_full_name',
            'team_abbr_name',
            'logo',
            'team_name',
            'team_wins_losses',
            'qtr_points',
            'point'
        ]

class GameSerializer(serializers.ModelSerializer):
    home_team_info = serializers.SerializerMethodField()
    away_team_info = serializers.SerializerMethodField()
    is_future_game = serializers.SerializerMethodField()
    game_status = serializers.CharField()
    game_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Game
        fields = [
            'game_id',
            'game_date',
            'game_status',
            'is_future_game',
            'home_team_info',
            'away_team_info'
        ]

    def get_home_team_info(self, obj):
        live_games = self.context.get('live_games', {})
        game_id = obj.game_id
        if game_id in live_games:
            team_wins_losses = live_games[game_id]["home_team_info"]["team_wins_losses"]
            qtr_points = live_games[game_id]["home_team_info"]["qtr_points"]
            point = live_games[game_id]["home_team_info"]["point"]
        else:
            team_wins_losses = obj.home_team_wins_losses
            qtr_points = []
            point = obj.home_total_points

        team = obj.home_team
        return {
            "team_id": team.id,
            "team_full_name": team.full_name,
            "team_abbr_name": team.abbrevation,
            "logo": team.logo,
            "team_name": team.name,
            "team_wins_losses": team_wins_losses,
            "qtr_points": qtr_points,
            "point": point
        }

    def get_away_team_info(self, obj):
        live_games = self.context.get('live_games', {})
        game_id = obj.game_id
        if game_id in live_games:
            team_wins_losses = live_games[game_id]["away_team_info"]["team_wins_losses"]
            qtr_points = live_games[game_id]["away_team_info"]["qtr_points"]
            point = live_games[game_id]["away_team_info"]["point"]
        else:
            team_wins_losses = obj.away_team_wins_losses
            qtr_points = []
            point = obj.away_total_points

        team = obj.away_team
        return {
            "team_id": team.id,
            "team_full_name": team.full_name,
            "team_abbr_name": team.abbrevation,
            "logo": team.logo,
            "team_name": team.name,
            "team_wins_losses": team_wins_losses,
            "qtr_points": qtr_points,
            "point": point
        }
    def get_is_future_game(self, obj):
        return obj.game_status == GameStatus.SCHEDULED
