# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.nba.utils import *
from apps.nba.models import Team
from nba_api.stats.static import teams

class Command(BaseCommand):
    help = 'Import Team'

    def handle(self, *args, **options):
        for team in teams.get_teams():
            logo_filename = team["full_name"].replace(" ", "")
            logo = static(f"assets/svg/nba_team_logo/{logo_filename}.svg")
            
            data = {
                "name": team["nickname"],
                "full_name": team["full_name"],
                "abbrevation": team["abbreviation"],
                "logo": logo
            }
            Team.objects.update_or_create(id=team["id"], defaults=data)
        
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
