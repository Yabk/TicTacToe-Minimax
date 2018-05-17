#!/usr/bin/python3
from game_backend import *
from copy import deepcopy
import random

nodes_visited = 0

class Minimax:
    def __init__(self, game, first=False):
        self.game = game
        self.first = first
        self.pruning = True


    def get_move(self):
        global nodes_visited
        moves = Minimax.next_level(self.game.board, self.first)
        scores = []
        nodes_visited = 0

        if self.pruning:
            a = -2
            b = 2
            best = -2
            for move in moves:
                score = Minimax.minimax_with_abpruning(move, False, self.first, a, b)
                best = max(best, score)
                scores.append(score)
                if best == 1:
                    return self.extract_move(move)

            best_moves = [x for x in moves if scores[moves.index(x)] == best]

            return self.extract_move(random.choice(best_moves))
        else:
            for move in moves:
                score, wins = Minimax.minimax(move, False, self.first)
                scores.append((score, wins))

            best_move = Minimax.best_move(scores, moves)
            return self.extract_move(best_move)


    def set_pruning(self, pruning):
        self.pruning = pruning


    def best_move(scores, moves):
        best_score = -2
        best_wins = -1
        for i in range(len(scores)):
            if scores[i][0] > best_score:
                best_score, best_wins = scores[i]
            elif scores[i][0] == best_score and scores[i][1] > best_wins:
                best_wins = scores[i][1]

        best_moves = []
        for i in range(len(scores)):
            if scores[i][0] == best_score and scores[i][1] == best_wins:
                best_moves.append(moves[i])

        return random.choice(best_moves)


    def move(self):
        return self.game.move(self.get_move())


    def move(self, row, column):
        return self.game.move(row, column)


    def extract_move(self, move):
        for row in range(3):
            for column in range(3):
                if self.game.board[row][column] != move[row][column]:
                    return row, column


    def setTurn(self, first):
        self.first = first


    def minimax(board, maximizing, player):
        global nodes_visited
        state = Game.check_game_state(board)
        if state != GameState.NOT_DONE:
            nodes_visited += 1
            if ((player and state == GameState.X_WIN) or
            ((not player) and state == GameState.Y_WIN)):
                return 1, 0
            elif state == GameState.DRAW:
                return 0, 0
            else:
                return -1, 0

        if maximizing:
            best = -2
            for node in Minimax.next_level(board, player):
                node_score = Minimax.minimax(node, False, player)[0]
                best = max(node_score, best)
            return best, 0
        else:
            best = 2
            wins = 0
            for node in Minimax.next_level(board, not player):
                node_score = Minimax.minimax(node, True, player)[0]
                wins += 1 if node_score == 1 else 0
                best = min(node_score, best)
            return best, wins


    def minimax_with_abpruning(board, maximizing, player, a, b):
        global nodes_visited
        state = Game.check_game_state(board)
        if state != GameState.NOT_DONE:
            nodes_visited += 1
            if ((player and state == GameState.X_WIN) or
            ((not player) and state == GameState.Y_WIN)):
                return 1
            elif state == GameState.DRAW:
                return 0
            else:
                return -1

        if maximizing:
            best = -2
            for node in Minimax.next_level(board, player):
                node_score = Minimax.minimax_with_abpruning(node, False, player, a, b)
                best = max(node_score, best)
                a = max(a, best)
                if a >= b:
                    return best
            return best
        else:
            best = 2
            for node in Minimax.next_level(board, not player):
                node_score = Minimax.minimax_with_abpruning(node, True, player, a, b)
                best = min(node_score, best)
                b = min(b, best)
                if b <= a:
                    return best
            return best


    def next_level(board, player):
        new_boards = []
        for row in range(3):
            for column in range(3):
                if board[row][column] is None:
                    new_board = deepcopy(board)
                    new_board[row][column] = player
                    new_boards.append(new_board)

        random.shuffle(new_boards)
        return new_boards
