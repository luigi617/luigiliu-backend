# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.nba.utils import *
from apps.nba.models import Team
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import ScoreboardV2
from datetime import datetime

class Command(BaseCommand):
    help = 'Import Team'

    def handle(self, *args, **options):
        a = fetch_nba_standings()
        
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
