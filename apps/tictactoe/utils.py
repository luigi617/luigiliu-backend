import numpy as np
import random
from apps.tictactoe.models import QValue  # Ensure this import is correct in your environment

def get_q_value(state, action):
    """
    Retrieve the Q-value from the database for a given state-action pair.
    If the Q-value does not exist, return 0.0.
    """
    try:
        q_value = QValue.objects.get(state=state, action=action).q_value
    except QValue.DoesNotExist:
        q_value = 0.0  # Default Q-value if not found
    return q_value

def update_q_value(state, action, new_q_value):
    """
    Update the Q-value in the database for a given state-action pair.
    If the pair does not exist, create it.
    """
    q_value_entry, created = QValue.objects.get_or_create(state=state, action=action)
    q_value_entry.q_value = new_q_value
    q_value_entry.save()

BOARD_ROWS = 3
BOARD_COLS = 3


def getHashBoard(board):
    return "|".join(str(int(x)) for x in board)

class TicTacToe:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.playerSymbol = -1


    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def updateState(self, position):
        self.board[position[0], position[1]] = self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    def check_win(self):
        for i in range(BOARD_ROWS):
            if np.all(self.board[i, :] == self.playerSymbol):
                return self.playerSymbol
            if np.all(self.board[:, i] == self.playerSymbol):
                return self.playerSymbol
        if np.all(np.diag(self.board) == self.playerSymbol):
            return self.playerSymbol
        if np.all(np.diag(np.fliplr(self.board)) == self.playerSymbol):
            return self.playerSymbol
        if not any(0 in row for row in self.board):
            return 0
        return None

    def giveReward(self):
        result = self.check_win()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.5)
            self.p2.feedReward(0.5)

    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 10 == 0:
                print("Rounds {}".format(i))
            while True:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # Take action and update board state
                self.updateState(p1_action)
                board_hash = getHashBoard(self.board.reshape(BOARD_ROWS * BOARD_COLS))
                self.p1.addState(board_hash, p1_action)
                win = self.check_win()
                if win is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = getHashBoard(self.board.reshape(BOARD_ROWS * BOARD_COLS))
                    self.p2.addState(board_hash, p2_action)
                    win = self.check_win()
                    if win is not None:
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def test(self, rounds=100):
        """
        Test the performance of the trained agent.
        """
        results = {self.p1.name: 0, self.p2.name: 0, 'draw': 0}
        for i in range(rounds):
            while True:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol, test=True)
                self.updateState(p1_action)
                win = self.check_win()
                if win is not None:
                    if win == 1:
                        results[self.p1.name] += 1
                    elif win == -1:
                        results[self.p2.name] += 1
                    else:
                        results['draw'] += 1
                    self.reset()
                    break
                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol, test=True)
                    self.updateState(p2_action)
                    win = self.check_win()
                    if win is not None:
                        if win == 1:
                            results[self.p1.name] += 1
                        elif win == -1:
                            results[self.p2.name] += 1
                        else:
                            results['draw'] += 1
                        self.reset()
                        break
        return results[self.p1.name], results[self.p2.name], results['draw'], rounds

class Agent:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.exp_rate = exp_rate
        self.lr = 0.2
        self.gamma = 0.9
        self.states_actions = []  # Stores tuples of (state, action)


    def chooseAction(self, positions, current_board, symbol, test=False):
        current_state = getHashBoard(current_board.reshape(BOARD_ROWS * BOARD_COLS))
        if not test and np.random.uniform(0, 1) <= self.exp_rate:
            # Exploration: choose a random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            # Exploitation: choose the action with the highest Q-value
            max_q_value = -np.inf
            for p in positions:
                action_str = str(p[0]*BOARD_ROWS + p[1])
                q_value = get_q_value(current_state, action_str)
                if q_value >= max_q_value:
                    max_q_value = q_value
                    action = p
            # If all Q-values are zero (unexplored), pick random action
            if max_q_value == 0:
                idx = np.random.choice(len(positions))
                action = positions[idx]
        self.states_actions.append((current_state, str(action[0]*BOARD_ROWS + action[1])))
        return action

    def addState(self, state, action):
        pass  # We already store states and actions in chooseAction

    def feedReward(self, reward):
        # Update Q-values in reverse order
        for state, action in reversed(self.states_actions):
            q_value = get_q_value(state, action)
            q_value_new = q_value + self.lr * (reward - q_value)
            update_q_value(state, action, q_value_new)
            reward = q_value_new
        self.states_actions = []

    def reset(self):
        self.states_actions = []

class RandomPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions, current_board, symbol, test=False):
        idx = np.random.choice(len(positions))
        return positions[idx]

    def addState(self, state, action):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass


