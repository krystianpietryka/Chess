#!/usr/bin/env python3
import os
import pygame
import PySimpleGUI as sg
import copy
import random
import Bots
import Game_move_logic
from Piece_class_stuff import Colour,  Sprites
# -------------------------------------PYGAME---------------------------------------------------------------------------


def Chess(game_type, player_colour):
    # Pygame Initialization
    pygame.init()
    # Pygame Sound Initialization
    pygame.mixer.init()
    s = "Sounds"
    move_sound = pygame.mixer.Sound(os.path.join(s, 'Move_sound.wav'))
    white = (255, 255, 255)    # RGB value for white
    x = 512
    y = 512
    display_surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption('Szachongi')

    # Game Logic variables
    object_dragging = False
    current_object = 0
    previous_row = 0
    previous_column = 0
    Game_move_logic.Move_allowance.current_turn = Colour.WHITE
    letters = ("a", "b", "c", "d", "e", "f", "g", "h")  # Used in converting move notation
    if player_colour == Colour.WHITE:
        bot_colour = Colour.BLACK
    else:
        bot_colour = Colour.WHITE
    # Blit the board and the pieces onto the Pygame display surface

    def Update_board_state(board):
        display_surface.blit(Sprites.board_image, (0, 0))
        for row in range(0, 8):
            for column in range(0, 8):
                cell = board[column][row]
                if cell != 0:   # If cell contains a piece, blit that piece
                    cell.column = column
                    cell.row = row
                    display_surface.blit(cell.model, (64 * row,  64 * column))
        pygame.display.flip()

    # Function highlights possible move locations for a piece (Blits red squares on coordinates)
    def Highlight_cells(cells):
        if cells is not None:
            for cell in cells:
                display_surface.blit(Sprites.Red_cell, (64 * cell[0], 64 * cell[1]))
            for row in range(0, 8):
                for column in range(0, 8):
                    cell = Game_move_logic.board[column][row]
                    if cell != 0:
                        cell.column = column
                        cell.row = row
                        display_surface.blit(cell.model, (64 * row, 64 * column))
            pygame.display.flip()

    Update_board_state(Game_move_logic.board)   # Initial Display
    print("Initializing")

    # Main game loop
    while True:
        if Game_move_logic.Move_allowance.checkmate == 1:
            break
        # BOT STUFF
        if game_type != 0 and Game_move_logic.Move_allowance.current_turn != player_colour:
            if game_type == 1:  # Random Bot
                bot_variables = Bots.Random_Bot(Game_move_logic.board, bot_colour)
                move = Game_move_logic.Move(Game_move_logic.board, bot_variables[0], bot_variables[1][0], bot_variables[1][1], bot_variables[0].row, bot_variables[0].column)
                if move[1] == 1:
                    current_turn = player_colour
                    pygame.time.wait(random.randint(300, 1200))
                    pygame.mixer.Sound.play(move_sound)
                    #print(letters[x] + str(y))
                else:
                    Game_move_logic.board = move[0]
                    current_turn = bot_colour
                Update_board_state(Game_move_logic.board)

            elif game_type == 2:    # NegaMax Bot
                bot_variables = Bots.NegaMax(3, Game_move_logic.board, bot_colour)
                move = Game_move_logic.Move(Game_move_logic.board, bot_variables[0], bot_variables[1][0],
                                            bot_variables[1][1], bot_variables[0].row, bot_variables[0].column)
                if move[1] == 1:
                    current_turn = player_colour
                    pygame.time.wait(random.randint(300, 1200))
                    pygame.mixer.Sound.play(move_sound)
                    # print(letters[x] + str(y))
                else:
                    Game_move_logic.board = move[0]
                    current_turn = bot_colour
                Update_board_state(Game_move_logic.board)

                return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Get piece at click coordinates
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x = int(x / 64)
                    y = int(y / 64)
                    piece = Game_move_logic.board[y][x]

                    # If piece exists and the turn colour matches, Highlights possible moves
                    if piece != 0:
                        if piece.colour == Game_move_logic.Move_allowance.current_turn:
                            if (game_type != 0 and Game_move_logic.Move_allowance.current_turn == player_colour) or game_type == 0:
                                Highlight_cells(Game_move_logic.Possible_moves(piece))

                    # If an object was clicked previously, move it and empty its previous position
                    if object_dragging:
                        if current_object != 0:
                            object_dragging = False
                            if (x, y) in Game_move_logic.Possible_moves(current_object):
                                move = Game_move_logic.Move(Game_move_logic.board, current_object, x, y, previous_row, previous_column)
                                Game_move_logic.board = move[0]
                                Update_board_state(Game_move_logic.board)
                                # If move succeeded all checks, update the board, zero the variables
                                if move[1] == 1:
                                    pygame.mixer.Sound.play(move_sound)
                                    current_object = 0
                                    previous_row = 0
                                    previous_column = 0
                                    Game_move_logic.current_turn = Game_move_logic.Swap_Turns(Game_move_logic.Move_allowance.current_turn)
                                    print("Score: ", Bots.Shannon_Evaluation(Game_move_logic.board))
                                else:
                                    Game_move_logic.board = move[0]
                                Update_board_state(Game_move_logic.board)
                            # Case if clicked cell is not possible for the piece to move to
                            else:
                                print('Disallowed move')
                                Update_board_state(Game_move_logic.board)
                                continue

                    else:  # If piece was clicked
                        #print(x, y)
                        if Game_move_logic.board[y][x] != 0:
                            if Game_move_logic.Move_allowance.current_turn == Game_move_logic.board[y][x].colour:  # Check turn order
                                object_dragging = True
                                current_object = Game_move_logic.board[y][x]  # store the piece clicked
                                previous_row = copy.deepcopy(current_object.row)
                                previous_column = copy.deepcopy(current_object.column)
                            else:
                                print('Current Turn = ' + str(Game_move_logic.Move_allowance.current_turn))
# ----------------------------------------------------------------------------------------------------------------------
# GUI


sg.theme('LightBrown10')
free_play = 0


def intro():
    layout = [[sg.Text('Welcome to my chess simulation!', size=(50, 1))],
              [sg.Button('Single Player', size=(35, 2))],
              [sg.Button('Multi Player', size=(35, 2))],
              [sg.Button('Exit', size=(35, 2))]]
    return sg.Window('intro', layout, finalize=True)


def Single_Player():
    layout = [[sg.Text('Single Player', size=(50, 1))],
              [sg.Button('Free Play', size=(35, 2))],
              [sg.Button('Random Bot', size=(35, 2))],
              [sg.Button('NegaMax Bot (work in progress)', size=(35, 2))],
              [sg.Button('Exit', size=(35, 2))]]
    return sg.Window('Single Player', layout, finalize=True)


def Choose_Player_Colour():
    layout = [[sg.Text('Choose the colour of your pieces:', size=(50, 1))],
              [sg.Button('White', size=(35, 2))],
              [sg.Button('Black', size=(35, 2))],
              [sg.Button('Exit', size=(35, 2))]]
    return sg.Window('Choose Player Colour', layout, finalize=True)


def Main():
    window1, window2 = intro(), None
    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            if window2:
                window2.close()
            else:
                window1.close()
            if window == window2:  # if closing win 2, mark as closed
                window2 = None
            elif window == window1:  # if closing win 1, exit program
                break
        elif event == 'Single Player' and not window2:
            print('Single')
            window2 = Single_Player()
            window1.close()
        elif event == 'Free Play':
            print("gra")
            window2.close()
            Chess(0, Colour.WHITE)
        elif event == 'Random Bot':
            print("gra")
            window2.close()
            Chess(1, Colour.WHITE)
        elif event == 'NegaMax Bot':
            print("gra")
            window2.close()
            Chess(2, Colour.WHITE)
    window.close()


if __name__ == "__main__":
    Main()
