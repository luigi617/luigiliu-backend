# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.nba.utils import *
from apps.nba.models import Team, Game, GameStatus, Conference, StandingTeam
from django.db import transaction



def import_games():
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
    



def import_standing():
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
            _, created = StandingTeam.objects.update_or_create(
                year=get_current_season(), team=team_obj, defaults=data
            )

