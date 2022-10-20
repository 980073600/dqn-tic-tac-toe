import math

EMPTY = 0
X = 1
O = 2


class MinMaxAgent:
    def __init__(self, side, game):
        self.game = game
        self.side = side
        self.board = game.board

    def get_action(self):
        print("get")
        final_move = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        best = -1000
        move = None
        for i in range(9):
            if self.game.board[i] == EMPTY:
                print(i)
                self.game.board[i] = self.side
                move = max(best, self.minimax(False))
                self.game.board[i] = EMPTY

            if move > best:
                move = i
                best = move

        final_move[move] = 1
        return final_move

    def get_other(self):
        if self.side == X:
            return O
        elif self.side == O:
            return X

    def minimax(self, is_max):
        done, x_win, o_win = self.game.is_over()
        #print(done, x_win, o_win)
        if done and not x_win and not o_win:
            #print("_______________")
            return 0

        if done:
            #print("*******************")
            return 10 if self.game.who_won() == self.side else -10

        if is_max:
            print(is_max)
            best = -1000
            for i in range(9):
                if self.game.board[i] == EMPTY:
                    self.game.board[i] = self.side
                    best = max(best, self.minimax(not is_max))
                    self.game.board[i] = EMPTY

            return best
        else:
            print(is_max)
            best = 1000
            for i in range(9):
                if self.game.board[i] == EMPTY:
                    print(i)
                    self.game.board[i] = self.side
                    best = min(best, self.minimax(not is_max))
                    self.game.board[i] = EMPTY

            return best
