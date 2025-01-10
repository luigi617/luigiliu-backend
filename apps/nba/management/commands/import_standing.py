# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.nba.utils import *
from apps.nba.models import Team, Game, GameStatus, Conference, StandingTeam
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

            standing_teams = fetch_nba_standings()
            for team in standing_teams:
                conference = Conference.EAST if team["conference"] == "east" else Conference.WEST
                
                team_obj = Team.objects.get(id=team["team_id"])
                data = {
                    "rank": team["rank"],
                    "conference": conference,
                    "pct": team["pct"],
                    "wins": team["wins"],
                    "losses": team["losses"],
                    "home_wins_losses": team["home"],
                    "away_wins_losses": team["away"],
                    "last10_wins_losses": team["ll10"],
                }
                defaults = {
                    "year": get_current_season(),
                    "team": team_obj
                }
                _, created = StandingTeam.objects.update_or_create(
                    year=get_current_season(), team=team_obj, defaults=data
                )
                print(created)
        
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
