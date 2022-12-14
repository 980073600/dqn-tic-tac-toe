from agent import Q_Agent
from game import TicTacToe
import time
from minmaxagent import MinMaxAgent

X = 1
O = 2


def train():
    n_draws = 0
    n_games = 0
    x_wins = 0
    o_wins = 0
    game = TicTacToe(800, 600)
    x = Q_Agent(O)
    o = MinMaxAgent(X, game)

    count = 1
    while True:
        if count % 2 != 0:
            state_old = x.get_state(game)
            final_move = x.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move, X)
            state_new = x.get_state(game)
            count += 1
            if done:
                if x_reward == 0:
                    n_draws += 1
                elif x_reward == 1:
                    x_wins += 1
                elif o_reward == 1:
                    o_wins += 1
                game.reset()
                n_games += 1
                count = 1
                if n_games > 500:
                    x.train_long_memory()

                print(n_games)

        else:
            final_move = o.get_action()
            x_reward, o_reward, done = game.play_move(final_move, O)
            count += 1
            if done:
                x.remember(o_reward)
                if x_reward == 0:
                    n_draws += 1
                elif x_reward == 1:
                    x_wins += 1
                elif o_reward == 1:
                    o_wins += 1
                game.reset()
                n_games += 1
                count = 1
                if n_games > 500:
                    x.train_long_memory()

                print(n_games)

        if n_games > 600 and n_games % 100 == 1:
            print("Draws: " + str(n_draws) + " X wins: " + str(x_wins) + " O wins: " + str(o_wins))
            x_wins = 0
            o_wins = 0
            n_draws = 0


if __name__ == '__main__':
    train()
