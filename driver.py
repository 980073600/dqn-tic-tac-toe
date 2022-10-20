from agent import Agent
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
    x = MinMaxAgent(X, game)
    o = MinMaxAgent(O, game)
    count = 1
    while True:
        if count % 2 != 0:
            final_move = x.get_action()
            x_reward, o_reward, done = game.play_move(final_move, X)
            count += 1
            if done:
                #o.remember(x_reward)
                if x_reward == 0:
                    n_draws += 1
                elif x_reward == 1:
                    x_wins += 1
                elif o_reward == 1:
                    o_wins += 1
                game.reset()
                n_games += 1
                count = 1
                #if n_games > 500:
                   # o.train_long_memory()

                print(n_games)

        else:
            final_move = o.get_action()
            x_reward, o_reward, done = game.play_move(final_move, O)
            count += 1
            '''
            state_old = o.get_state(game)
            final_move = o.get_action(state_old)
            x_reward, o_reward, done = game.play_move(final_move, O)
            state_new = o.get_state(game)
            '''
            if done:
                #o.remember(o_reward)
                if x_reward == 0:
                    n_draws += 1
                elif x_reward == 1:
                    x_wins += 1
                elif o_reward == 1:
                    o_wins += 1
                game.reset()
                n_games += 1
                count = 1
                #if n_games > 500:
                    #o.train_long_memory()

                print(n_games)

       #if n_draws == 100:
            #o.q_net.save()

        if n_games > 600 and n_games % 100 == 1:
            print("Draws: " + str(n_draws) + " X wins: " + str(x_wins) + " O wins: " + str(o_wins))
            x_wins = 0
            o_wins = 0
            n_draws = 0

        #if n_games > 500:
        time.sleep(1)


if __name__ == '__main__':
    train()
