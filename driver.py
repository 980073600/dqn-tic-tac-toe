from agent import Agent
from game import TicTacToe
import time

X = 1
O = 2


def train():
    n_draws = 0
    n_games = 0
    x_wins = 0
    o_wins = 0
    x = Agent(X)
    o = Agent(O)
    game = TicTacToe(800, 600)
    count = 1
    while True:
        if count % 2 != 0:
            state_old = x.get_state(game)
            final_move = x.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move, X)
            state_new = x.get_state(game)
            count += 1

            if done:
                x.remember(x_reward)
                o.remember(o_reward)
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
                    o.train_long_memory()

                print(n_games)

        else:
            state_old = o.get_state(game)
            final_move = o.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move, O)
            state_new = o.get_state(game)
            #if n_games > 500:
                #o.train_short_memory(state_old, final_move, x_reward, state_new, done)
            #o.remember(o_reward)
            count += 1

            if done:
                x.remember(x_reward)
                o.remember(o_reward)
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
                    o.train_long_memory()

                print(n_games)

        if n_draws == 100:
            o.q_net.save()

        if n_games > 600 and n_games % 100 == 1:
            print("Draws: " + str(n_draws) + " X wins: " + str(x_wins) + " O wins: " + str(o_wins))
            x_wins = 0
            o_wins = 0
            n_draws = 0

        if n_games > 16400:
            time.sleep(1)


if __name__ == '__main__':
    train()
