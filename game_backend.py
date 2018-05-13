#!/usr/bin/python3
from enum import Enum


class IllegalMoveException(Exception):
    pass


class GameState(Enum):
    X_WIN = 1
    Y_WIN = 2
    DRAW = 3
    NOT_DONE = 4

    def win_state(x_player):
        if x_player:
            return GameState.X_WIN
        else:
            return GameState.Y_WIN


class Game:

    def __init__(self):
        self.board = [[None, None, None] for i in range(3)]
        self.turn = True
        self.state = GameState.NOT_DONE


    def move(self, row, column):
        if self.state != GameState.NOT_DONE:
            raise IllegalMoveException("Game is finished!")
        if self.board[row][column] is not None:
            raise IllegalMoveException("Field already taken!")

        self.board[row][column] = self.turn
        self.turn = not self.turn

        self.state = Game.check_game_state(self.board)
        return self.state


    def reset(self):
        self.board = [[None, None, None] for i in range(3)]
        self.turn = True
        self.state = GameState.NOT_DONE


    def check_game_state(board):
        win = None

        for row in board:
            if row[0] == row[1] == row[2] != None:
                return GameState.win_state(row[0])

        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] != None:
                return GameState.win_state(board[0][i])

        if board[0][0] == board[1][1] == board[2][2] != None:
            return GameState.win_state(board[0][0])
        if board[0][2] == board[1][1] == board[2][0] != None:
            return GameState.win_state(board[0][2])

        if Game.is_done(board):
            return GameState.DRAW

        return GameState.NOT_DONE


    def is_done(board):
        done = True
        for row in board:
            if None in row:
                done = False
        return done
