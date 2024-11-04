# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.tictactoe.utils import *
from apps.tictactoe.models import QValue

class Command(BaseCommand):
    help = 'Train the Tic-Tac-Toe agent'

    def handle(self, *args, **options):
        agent = Agent("Agent")
        human = Agent("Human")

        training_instance1 = TicTacToe(agent, human)
        print("Training the agent...")
        training_instance1.play(rounds=100000)
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
