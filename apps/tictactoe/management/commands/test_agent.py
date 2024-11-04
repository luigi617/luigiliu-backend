# rl_agent/management/commands/train_agent.py

from django.core.management.base import BaseCommand
from apps.tictactoe.utils import *  # Make sure train_agent is implemented in utils.py

class Command(BaseCommand):
    help = 'Train the Tic-Tac-Toe agent'

    def handle(self, *args, **options):
        # Instantiate players
        agent = Agent("Agent")
        opp = Agent("Opp")

        # Start the game
        test_instance = TicTacToe(agent, opp)

        # Testing the agent
        agent.exp_rate = 0  # Turn off exploration during testing
        self.stdout.write("\nTesting the agent against a random player...")
        wins, losses, draws, episodes = test_instance.test(rounds=1000)


        self.stdout.write(self.style.SUCCESS('Training completed successfully'))
        self.stdout.write(f"\nResults over {episodes} games:")
        self.stdout.write(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
        self.stdout.write(f"Win Rate: {wins / episodes * 100:.2f}%")
        self.stdout.write(f"Draw Rate: {draws / episodes * 100:.2f}%")
        self.stdout.write(f"Loss Rate: {losses / episodes * 100:.2f}%")
