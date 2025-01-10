from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError



class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    abbrevation = models.CharField(max_length=100)
    logo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'NBA Team'
        verbose_name_plural = 'NBA Teams'

class GameStatus(models.TextChoices):
    FINAL = 'Final', 'Final'
    SCHEDULED = 'Scheduled', 'Scheduled'
    INPROGRESS = 'In Progress', 'In Progress'

class Game(models.Model):
    game_id = models.CharField(max_length=20, primary_key=True)
    game_date = models.DateTimeField()
    game_status = models.CharField(max_length=15, choices=GameStatus.choices)

    # Home Team Information
    home_team = models.ForeignKey(
        Team,
        related_name='home_games',
        on_delete=models.CASCADE
    )
    home_team_wins_losses = models.CharField(max_length=10)

    home_total_points = models.PositiveIntegerField()

    # Away Team Information
    away_team = models.ForeignKey(
        Team,
        related_name='away_games',
        on_delete=models.CASCADE
    )
    away_team_wins_losses = models.CharField(max_length=10)
    away_total_points = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.game_date}"

    class Meta:
        ordering = ['-game_date']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
    

class Conference(models.TextChoices):
    EAST = 'East', 'East'
    WEST = 'West', 'West'

class StandingTeam(models.Model):
    year = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    rank = models.PositiveIntegerField()

    conference = models.CharField(
        max_length=5,
        choices=Conference.choices
    )
    
    pct = models.DecimalField(max_digits=5, decimal_places=3)
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    
    home_wins_losses = models.CharField(max_length=10)
    away_wins_losses = models.CharField(max_length=10)
    
    last10_wins_losses = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.team.name} at n. {self.rank} ({self.conference}) - {self.year}"

    class Meta:
        unique_together = ('year', 'team')
        verbose_name = 'NBA Team Standing'
        verbose_name_plural = 'NBA Team Standings'
