import torch
import random
import numpy as np
from net import Net, Trainer
from game import TicTacToe
from collections import deque
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 60
LR = 0.01
X = 1
O = 2


class Agent:
    def __init__(self, side):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.99
        self.memory = deque(maxlen=MAX_MEMORY)
        self.q_net = Net()
        self.target_net = Net()
        self.trainer = Trainer(self.q_net, self.target_net, lr=LR, gamma=self.gamma)
        self.pieces = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.side = side
        self.action_log = []
        self.board_state_log = []

    def get_other(self):
        if self.side == X:
            return O
        elif self.side == O:
            return X

    def get_state(self, game):

        state = np.array([(self.pieces),
                          (game.get_side(self.get_other())),
                          (game.get_empty())])
        state = state.reshape(3, 3, 3)
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.board_state_log.append(state)
        self.epsilon = 0
        if self.n_games > 500:
            self.epsilon = 160 - (self.n_games - 500)
        final_move = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        if random.randint(0, 200) < self.epsilon or self.n_games < 500:
            r = random.randint(0, 2)
            c = random.randint(0, 2)
            while state[2, r, c] == 0:
                r = random.randint(0, 2)
                c = random.randint(0, 2)

            final_move[(3 * r) + c] = 1
        else:
            print("*")
            state0 = torch.tensor(state, dtype=torch.float)
            actions = self.q_net.forward(state0)
            action = torch.argmax(actions).item()

            while state[action] != 0:
                i = 0
                for e in actions:
                    if e == torch.max(actions):
                        idx = i
                    i += 1

                actions[idx] = -100
                action = torch.argmax(actions).item()
            final_move[action] = 1

        self.action_log.append(final_move)
        return final_move

    def get_logs(self):
        return self.action_log, self.board_state_log

