X = 1
O = 2

class MinMaxAgent():

    def __init__(self, side):
        self.side = side
        self.cache = {}

    def move(self):
         pass

    def get_other(self):
        if self.side == X:
            return O
        elif self.side == O:
            return X

    def min(self, game, board):
        hash_value = game.hash_value_value()
        if hash_value in self.cache:
            return self.cache[hash_value]

        min_value = 0
        action = -1

        b = game.board

        res = self.max(game, b)
        winner = game.who_won()
        if self.side == winner:
            min_value = 1
            action = -1
        elif self.get_other() == winner:
            min_value = -1
            action = -1
        else:
            for index in [i for i, e in enumerate(board) if board[i] == 0]:
                if res < min_value or action == -1:
                    min_value = res
                    action = index

                    if min_value == -1:
                        self.cache[hash_value] = (min_value, action)
                        return min_value, action

                self.cache[hash_value] = (min_value, action)
        return min_value, action

    def max(self, game, board):
        hash_value = game.hash_value_value()
        if hash_value in self.cache:
            return self.cache[hash_value]

        max_value = 0
        action = -1

        b = game.board

        res = self.max(game, b)
        winner = game.who_won()
        if self.side == winner:
            max_value = 1
            action = -1
        elif self.get_other() == winner:
            max_value = -1
            action = -1
        else:
            for index in [i for i, e in enumerate(board) if board[i] == 0]:
                if res > max_value or action == -1:
                    max_value = res
                    action = index

                    if max_value == 1:
                        self.cache[hash_value] = (max_value, action)
                        return max_value, action

                self.cache[hash_value] = (max_value, action)
        return max_value, action