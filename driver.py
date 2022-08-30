import torch
import numpy as np
from agent import Agent
from game import TicTacToe
import time

X = 1
O = 2

def train():
    n_games = 0
    x = Agent(X)
    o = Agent(O)
    game = TicTacToe(800, 600)
    while True:
        if game.move % 2 != 0:
            state_old = x.get_state(game)
            final_move = x.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move)
            state_new = x.get_state(game)
            if n_games > 500:
                x.train_short_memory(state_old, x_reward, final_move, state_new, done)
            x.remember(state_old, final_move, x_reward, state_new, done)
        else:
            state_old = o.get_state(game)
            final_move = o.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move)
            state_new = o.get_state(game)
            if n_games > 500:
                o.train_short_memory(state_old, o_reward, final_move, state_new, done)
            o.remember(state_old, final_move, o_reward, state_new, done)

        if done:
            game.reset()
            n_games += 1
            if n_games > 501:
                x.train_long_memory()
                o.train_long_memory()

            print("Game: ", n_games)

        if n_games > 1000:
            time.sleep(1)


if __name__ == '__main__':
    train()
