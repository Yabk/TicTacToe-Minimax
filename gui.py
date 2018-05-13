#!/usr/bin/python3
import tkinter as tk
from tkinter import font
from functools import partial
from game_backend import *
from minimax_bot import Minimax
import minimax_bot
from timeit import default_timer as timer

game = Game()
bot = Minimax(game)
running = False
locked = []
FIRST = player_label = 'X'
SECOND = bot_label = 'O'

def play(row, column):
    lock_all()
    buttons[row][column].config(text=player_label)
    state = game.move(row, column)
    locked.append(buttons[row][column])

    if state == GameState.NOT_DONE:
        bot_play_button.config(state='active')
    else:
        lock_all()


def new_game(bot_first):
    global player_label, bot_label, locked

    lock_all()

    bot.setTurn(bot_first)
    game.reset()
    player_label = SECOND if bot_first else FIRST
    bot_label = FIRST if bot_first else SECOND
    locked = []

    for row in buttons:
        for button in row:
            button.config(text='')

    if bot_first:
        bot_play_button.config(state='active')

    else:
        bot_play_button.config(state='disabled')
        unlock()


def bot_make_turn():
    bot_play_button.config(state='disabled')
    start = timer()
    row, column = bot.get_move()
    end = timer()
    time_label.config(text='time: {}'.format(end-start))
    nodes_visited_label.config(text='leaf nodes: '+str(minimax_bot.nodes_visited))
    locked.append(buttons[row][column])
    buttons[row][column].config(text=bot_label)
    state = bot.move(row, column)

    if state == GameState.NOT_DONE:
        unlock()


def lock_all():
    for row in buttons:
        for button in row:
            button.config(state='disabled')


def unlock():
    for row in buttons:
        for button in row:
            if button not in locked:
                button.config(state='active')


def toggle_pruning():
    bot.pruning = not bot.pruning
    if bot.pruning:
        pruning_label.config(text='Pruning: on')
    else:
        pruning_label.config(text='Pruning: off')


root = tk.Tk()
root.geometry('500x500')
root.title('TicTacToe')
menu_window = tk.Tk()
menu_window.title('Menu')
font = font.Font(family='Helvetica', size=20, weight=font.BOLD)
pixel = tk.PhotoImage(width=0, height=0)

#menu
start_label = tk.Label(menu_window, text='Bot goes first?')
bot_play_button = tk.Button(menu_window, text='BOT PLAY', command=bot_make_turn, state='disabled')
bot_play_button.pack(fill=tk.X)
start_label.pack(fill=tk.X)
menu_subframe1 = tk.Frame(menu_window)
menu_subframe1.pack(fill=tk.X)
bot_first = tk.Button(menu_subframe1, text='Y', width=5, command=partial(new_game, True))
player_first = tk.Button(menu_subframe1, text='N', width=5, command=partial(new_game, False))
bot_first.pack(side=tk.LEFT)
player_first.pack(side=tk.RIGHT)
pruning_label = tk.Label(menu_window, text='Pruning: on')
pruning_label.pack(fill=tk.X)
pruning_button = tk.Button(menu_window, text='on/off', command=toggle_pruning)
pruning_button.pack(fill=tk.X)
time_label = tk.Label(menu_window, text='time: ')
time_label.pack(fill=tk.X)
nodes_visited_label = tk.Label(menu_window, text='leaf nodes: ')
nodes_visited_label.pack(fill=tk.X)

#game
buttons = []
for row in range(3):
    tk.Grid.rowconfigure(root, row, weight=1)
    buttons.append([])
    for column in range(3):
        tk.Grid.columnconfigure(root, column, weight=1)
        button = tk.Button(root, text='', font=font, compound='center',
            command=partial(play, row, column), state='disabled')
        button.grid(row=row, column=column, sticky=tk.N+tk.S+tk.E+tk.W)
        buttons[row].append(button)

root.mainloop()
