#!/usr/bin/python3
from game_backend import *
import minimax_bot


def main():
    g = Game()
    bot = minimax_bot.Minimax(g, False)

    end = False

    while not end:
        bot_turn = input("Bot goes first? [y/n] : ")[0] == 'y'
        bot.setTurn(bot_turn)
        g.reset()

        while g.state == GameState.NOT_DONE:
            bot_turn = next_turn(g, bot, bot_turn)
            print_board(g.board)

        print_ending(g.state)

        end = input("Go again? [y/n] : ")[0] == 'n'


def next_turn(game, bot, bot_turn):
    if bot_turn:
        row, column = bot.get_move()
        print()
        input("Press enter")
        print()
        print("Bot plays ({}, {})".format(row + 1, column + 1))
        bot.move(row, column)
    else:
        print()
        str_input = input("Your turn (row column) : ")
        row, column = [int(x) for x in str_input.split()]
        game.move(row - 1, column - 1)

    return not bot_turn


def print_board(board):
    print_row(board[0])
    print('-+-+-')
    print_row(board[1])
    print('-+-+-')
    print_row(board[2])


def print_row(row):
    printing_row = []
    for element in row:
        if element is None:
            printing_row.append(' ')
        elif element:
            printing_row.append('X')
        else:
            printing_row.append('O')

    print('{}|{}|{}'.format(printing_row[0], printing_row[1], printing_row[2]))


def print_ending(state):
    print()
    if state == GameState.DRAW:
        print("DRAW")
    elif state == GameState.X_WIN:
        print("X WINS")
    elif state == GameState.Y_WIN:
        print("O WINS")
    print()


if __name__ == '__main__':
    main()
