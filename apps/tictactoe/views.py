# rl_agent/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.tictactoe.models import QValue
from .utils import get_q_value, update_q_value
import random

class GetNextActionView(APIView):
    def post(self, request):
        state = request.data.get('state')
        player = request.data.get('player', 1)  # 1 for RL agent, -1 for opponent
        available_actions = request.data.get('available_actions')  # List of available cells (0-8)

        if state is None or available_actions is None:
            return Response({"error": "State and available actions are required."}, status=status.HTTP_400_BAD_REQUEST)

        print(state, available_actions)
        # Retrieve Q-values for each available action
        q_values = {action: get_q_value(state, action) for action in available_actions}
        
        # Choose the action with the highest Q-value
        best_action = max(q_values, key=q_values.get)


        return Response({"next_action": best_action})