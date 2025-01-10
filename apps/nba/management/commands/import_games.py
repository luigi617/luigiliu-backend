# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.nba.utils import *
from apps.nba.models import Team, Game, GameStatus
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import ScoreboardV2
from datetime import datetime
from django.db import transaction

class Command(BaseCommand):
    help = 'Import Team'

    def handle(self, *args, **options):
        # team_info = get_team_information()
        # print(team_info.keys())
        with transaction.atomic():

            games = get_all_games()
            for game in games:
                status = None
                if game["game_status"] == 1:
                    status = GameStatus.SCHEDULED
                elif game["game_status"] == 2:
                    status = GameStatus.INPROGRESS
                else:
                    status = GameStatus.FINAL
                home_team = Team.objects.get(id=game["home_team_info"]["team_id"])
                away_team = Team.objects.get(id=game["away_team_info"]["team_id"])
                data = {
                    "game_date": game["game_date"],
                    "game_status": status,
                    "home_team": home_team,
                    "home_team_wins_losses": game["home_team_info"]["team_wins_losses"],
                    "home_total_points": game["home_team_info"]["point"],
                    "away_team": away_team,
                    "away_team_wins_losses": game["away_team_info"]["team_wins_losses"],
                    "away_total_points": game["away_team_info"]["point"],
                }
                Game.objects.update_or_create(game_id=game["game_id"], defaults=data)
        
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
