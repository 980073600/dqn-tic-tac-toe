import torch
import random
import numpy as np
from net import Net, Trainer
from collections import deque
import torch.nn.functional as F


MAX_MEMORY = 100_000
BATCH_SIZE = 60
LR = 0.01
X = 1
O = 2


class Agent:
    def __init__(self, side):
        self.n_games = 0
        self.epsilon = 0.9999
        self.epsilon_decrease = 0.9997
        self.gamma = 0.99
        self.win_memory = deque(maxlen=MAX_MEMORY)
        self.draw_memory = deque(maxlen=MAX_MEMORY)
        self.loss_memory = deque(maxlen=MAX_MEMORY)
        self.q_net = Net()
        self.target_net = Net()
        self.trainer = Trainer(self.q_net, self.target_net, lr=LR, gamma=self.gamma)
        self.pieces = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.side = side
        self.action_log = []
        self.board_position_log = []

    def get_other(self):
        if self.side == X:
            return O
        elif self.side == O:
            return X

    def get_state(self, game):
        state = np.array([self.pieces.astype(int),
                          (game.get_side(self.get_other())).astype(int),
                          (game.get_empty()).astype(int)])
        state = state.reshape(3, 3, 3)
        state = np.transpose(state, [0, 1, 2])
        self.board_position_log.append(state.copy())
        return state

    def remember(self, reward):
        length = len(self.action_log)
        if reward == 1:
            memory = self.win_memory
        elif reward == 0:
            memory = self.draw_memory
        else:
            memory = self.loss_memory

        for i in range(length - 1):
            memory.append((self.board_position_log[i], self.action_log[i], 0, self.board_position_log[i + 1], False))

        memory.append((self.board_position_log[length - 1], self.action_log[length - 1], reward, np.array(([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]])), True))
        self.board_position_log = []
        self.action_log = []

    def train_long_memory(self):
        BATCH_THIRD = 20
        batch = random.sample(self.win_memory, BATCH_THIRD)
        batch.extend(random.sample(self.draw_memory, BATCH_THIRD))
        batch.extend(random.sample(self.loss_memory, BATCH_THIRD))

        states, actions, rewards, next_states, dones = zip(*batch)
        self.epsilon *= self.epsilon_decrease
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 0
        if self.n_games > 500:
            self.epsilon = 0.9999
        final_move = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        action = 0
        if random.random() > self.epsilon:
            r = random.randint(0, 2)
            c = random.randint(0, 2)
            while state[2, r, c] == 0:
                r = random.randint(0, 2)
                c = random.randint(0, 2)

            final_move[(3 * r) + c] = 1
            action = (3 * r) + c
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            actions = self.q_net.forward(state0)
            actions = F.softmax(actions)

            while state[action] != 0:
                i = 0
                for e in actions:
                    if e == torch.max(actions):
                        idx = i
                    i += 1

                actions[idx] = -1
                action = torch.argmax(actions).item()
            final_move[action] = 1

        self.action_log.append(action)
        return final_move
