import pygame
import numpy as np
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X = 1
O = 2
EMPTY = 0

pygame.init()


class TicTacToe:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((w, h))
        self.display.fill(WHITE)
        pygame.display.set_caption("Tic Tac Toe")
        self.x_wins = 0
        self.o_wins = 0
        self.reset()

    def get_side(self, side):
        arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        idx = 0
        if side == X:
            for i in self.board:
                if i == 1:
                    arr[idx] = 1
                idx += 1
        elif side == O:
            for i in self.board:
                if i == 2:
                    arr[idx] = 1
                idx += 1

        return arr

    def get_empty(self):
        idx = 0
        arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i in self.board:
            if i == 0:
                arr[idx] = 1
            idx += 1

        return arr

    def reset(self):
        self.move = 1
        self.board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.display.fill(WHITE)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(0, self.h / 3, self.w, 25))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(0, self.h * (2 / 3), self.w, 25))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.w / 3, 0, 25, self.h))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.w * (2 / 3), 0, 25, self.h))
        # self.update_ui()

    def update_ui(self):
        i = 0
        for s in self.board:
            if s == X:
                if i == 0:
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.1, (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.9, (self.h / 3) * 0.9))
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.9, (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.1, (self.h / 3) * 0.9))

                elif i == 1:
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.9))
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.9))

                elif i == 2:
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.9))
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.1),
                                     ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.9))

                elif i == 3:
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.1, (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.9, (self.h / 3) * 0.9 + (self.h / 3)))
                    pygame.draw.line(self.display, BLACK, ((self.w / 3) * 0.9, (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.1, (self.h / 3) * 0.9 + (self.h / 3)))

                elif i == 4:
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.9 + (self.h / 3)))
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.9 + (self.h / 3)))

                elif i == 5:
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.9 + (self.h / 3)))
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.1 + (self.h / 3)),
                                     ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.9 + (self.h / 3)))

                elif i == 6:
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.1, (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.9, (self.h / 3) * 0.9 + (2 * (self.h / 3))))
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.9, (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.1, (self.h / 3) * 0.9 + (2 * (self.h / 3))))

                elif i == 7:
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.9 + (2 * (self.h / 3))))
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.9 + (self.w / 3), (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.1 + (self.w / 3), (self.h / 3) * 0.9 + (2 * (self.h / 3))))

                elif i == 8:
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.9 + (2 * (self.h / 3))))
                    pygame.draw.line(self.display, BLACK,
                                     ((self.w / 3) * 0.9 + (2 * (self.w / 3)), (self.h / 3) * 0.1 + (2 * (self.h / 3))),
                                     ((self.w / 3) * 0.1 + (2 * (self.w / 3)), (self.h / 3) * 0.9 + (2 * (self.h / 3))))
            elif s == O:
                if i == 0:
                    pygame.draw.circle(self.display, BLACK, (self.w / 6, self.h / 6), 75, 1)

                elif i == 1:
                    pygame.draw.circle(self.display, BLACK, (self.w / 2, self.h / 6), 75, 1)

                elif i == 2:
                    pygame.draw.circle(self.display, BLACK, (self.w * (5 / 6), self.h / 6), 75, 1)

                elif i == 3:
                    pygame.draw.circle(self.display, BLACK, (self.w / 6, self.h / 2), 75, 1)

                elif i == 4:
                    pygame.draw.circle(self.display, BLACK, (self.w / 2, self.h / 2), 75, 1)

                elif i == 5:
                    pygame.draw.circle(self.display, BLACK, (self.w * (5 / 6), self.h / 2), 75, 1)

                elif i == 6:
                    pygame.draw.circle(self.display, BLACK, (self.w / 6, self.h * (5 / 6)), 75, 1)

                elif i == 7:
                    pygame.draw.circle(self.display, BLACK, (self.w / 2, self.h * (5 / 6)), 75, 1)

                elif i == 8:
                    pygame.draw.circle(self.display, BLACK, (self.w * (5 / 6), self.h * (5 / 6)), 75, 1)

            i += 1

        pygame.display.flip()

    def play_move(self, action, side):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if np.array_equal(action, [1, 0, 0, 0, 0, 0, 0, 0, 0]):
            if self.board[0] == EMPTY:
                self.board[0] = side

        if np.array_equal(action, [0, 1, 0, 0, 0, 0, 0, 0, 0]):
            if self.board[1] == EMPTY:
                self.board[1] = side

        if np.array_equal(action, [0, 0, 1, 0, 0, 0, 0, 0, 0]):
            if self.board[2] == EMPTY:
                self.board[2] = side

        if np.array_equal(action, [0, 0, 0, 1, 0, 0, 0, 0, 0]):
            if self.board[3] == EMPTY:
                self.board[3] = side

        if np.array_equal(action, [0, 0, 0, 0, 1, 0, 0, 0, 0]):
            if self.board[4] == EMPTY:
                self.board[4] = side

        if np.array_equal(action, [0, 0, 0, 0, 0, 1, 0, 0, 0]):
            if self.board[5] == EMPTY:
                self.board[5] = side

        if np.array_equal(action, [0, 0, 0, 0, 0, 0, 1, 0, 0]):
            if self.board[6] == EMPTY:
                self.board[6] = side

        if np.array_equal(action, [0, 0, 0, 0, 0, 0, 0, 1, 0]):
            if self.board[7] == EMPTY:
                self.board[7] = side

        if np.array_equal(action, [0, 0, 0, 0, 0, 0, 0, 0, 1]):
            if self.board[8] == EMPTY:
                self.board[8] = side

        self.update_ui()

        x_reward = 0
        o_reward = 0
        game_over, x_win, o_win = self.is_over()
        if game_over:
            if x_win:
                x_reward = 1
                o_reward = -1
            elif o_win:
                x_reward = -1
                o_reward = 1

            self.reset()

            return x_reward, o_reward, game_over

        self.move += 1
        return x_reward, o_reward, game_over

    def is_over(self):
        x_win = False
        o_win = False

        if self.board[0] == self.board[1] and self.board[1] == self.board[2]:
            if self.board[0] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[0] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[3] == self.board[4] and self.board[4] == self.board[5]:
            if self.board[3] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[3] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[6] == self.board[7] and self.board[7] == self.board[8]:
            if self.board[6] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[6] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[0] == self.board[3] and self.board[3] == self.board[6]:
            if self.board[0] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[0] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[1] == self.board[4] and self.board[4] == self.board[7]:
            if self.board[1] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[1] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[2] == self.board[5] and self.board[5] == self.board[8]:
            if self.board[2] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[2] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            if self.board[0] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[0] == O:
                o_win = True
                return True, x_win, o_win
        if self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            if self.board[2] == X:
                x_win = True
                return True, x_win, o_win
            if self.board[2] == O:
                o_win = True
                return True, x_win, o_win

        if self.move == 9:
            x_win = False
            o_win = False
            return True, x_win, o_win

        return False, x_win, o_win
