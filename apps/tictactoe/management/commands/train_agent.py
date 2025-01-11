# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.tictactoe.utils import *
from apps.tictactoe.models import QValue

class Command(BaseCommand):
    help = 'Train the Tic-Tac-Toe agent'

    def add_arguments(self, parser):
        """
        add_arguments allows you to specify command-line options and arguments.
        """

        # Optional argument
        parser.add_argument(
            '--p1', 
            type=float, 
            default=1, 
            help='Number of times to print the greeting'
        )
        parser.add_argument(
            '--p2', 
            type=float, 
            default=1, 
            help='Number of times to print the greeting'
        )

    def handle(self, *args, **options):
        p1 = options['p1']
        p2 = options['p2']
        if p1 < 0 or p1 > 1:
            self.stdout.write(self.style.ERROR('p1 must be between 0 and 1.'))
            return
        if p2 < 0 or p2 > 1:
            self.stdout.write(self.style.ERROR('p2 must be between 0 and 1.'))
            return
        agent = Agent("Agent", exp_rate=p1)
        human = Agent("Human", exp_rate=p2)

        training_instance1 = TicTacToe(agent, human)
        print("Training the agent...")
        training_instance1.play(rounds=10000)
        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
