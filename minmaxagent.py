import math

EMPTY = 0
X = 1
O = 2


class MinMaxAgent:
    def __init__(self, side, game):
        self.game = game
        self.side = side
        self.cache = {}
        self.board = game.board

    def get_action(self, x):
        final_move = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        best_score = -math.inf
        best_move = None
        self.board = self.game.board
        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = self.side
                score = self.minmax(not x)
                self.board[i] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = i
        final_move[best_move] = 1
        return final_move

    def get_other(self):
        if self.side == X:
            return O
        elif self.side == O:
            return X

    def minmax(self, turn):
        done, o_win, x_win = self.game.is_over()
        if not o_win and not x_win and done:
            return 0

        elif done:
            return 1 if self.game.who_won() is self.side else -1

        scores = []
        self.board = self.game.board
        for i in range(9):
            if self.board[i] == 0:
                self.board[i] = self.side
                scores.append(self.minmax(not turn))
                self.board[i] = 0

        return max(scores) if turn else min(scores)
