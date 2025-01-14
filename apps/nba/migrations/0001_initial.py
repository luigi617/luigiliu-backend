# Generated by Django 4.0.3 on 2025-01-10 00:10

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('abbrevation', models.CharField(max_length=100)),
                ('logo', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'NBA Team',
                'verbose_name_plural': 'NBA Teams',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('game_date', models.DateField()),
                ('game_status', models.CharField(choices=[('Final', 'Final'), ('Scheduled', 'Scheduled'), ('In Progress', 'In Progress')], max_length=15)),
                ('home_team_wins_losses', models.CharField(max_length=10)),
                ('home_qtr_points', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), help_text='Points scored by the home team in each of the quarters.', size=None)),
                ('home_total_points', models.PositiveIntegerField()),
                ('away_team_wins_losses', models.CharField(max_length=10)),
                ('away_qtr_points', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), help_text='Points scored by the away team in each of the quarters.', size=None)),
                ('away_total_points', models.PositiveIntegerField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='nba.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='nba.team')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
                'ordering': ['-game_date'],
            },
        ),
        migrations.CreateModel(
            name='StandingTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10)),
                ('rank', models.PositiveIntegerField()),
                ('conference', models.CharField(choices=[('East', 'East'), ('West', 'West')], max_length=5)),
                ('pct', models.DecimalField(decimal_places=3, max_digits=5)),
                ('wins', models.PositiveIntegerField()),
                ('losses', models.PositiveIntegerField()),
                ('home_wins_losses', models.CharField(max_length=10)),
                ('away_wins_losses', models.CharField(max_length=10)),
                ('last10_wins_losses', models.CharField(max_length=10)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nba.team')),
            ],
            options={
                'verbose_name': 'NBA Team Standing',
                'verbose_name_plural': 'NBA Team Standings',
                'unique_together': {('year', 'team')},
            },
        ),
    ]
