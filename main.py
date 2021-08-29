#!/usr/bin/env python3
import os
import pygame
import copy
import Game_move_logic
from Piece_class_stuff import Colour, Piece_Objects, Sprites

# -------------------------------------PYGAME---------------------------------------------------------------------------
if __name__ == "__main__":
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
    move_row = 0
    move_column = 0
    previous_row = 0
    previous_column = 0
    current_turn = Colour.WHITE

    # Blit the board and the pieces onto the Pygame display surface
    def Update_board_state(board):
        display_surface.blit(Sprites.board_image, (0, 0))
        for row in range(0, 8):
            for column in range(0, 8):
                cell = board[column][row]
                if cell != 0:   # If cell contains a piece, blit that piece
                    cell.column = column
                    cell.row = row
                    display_surface.blit(cell.model, (64 * row, 64 * column))
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


    Update_board_state(Game_move_logic.board)  # Initial Display
    print("Initializing")

    # Main game loop
    while True:
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
                        if piece.colour == current_turn:
                            Highlight_cells(Game_move_logic.Possible_moves(piece))

                    # If an object was clicked previously, move it and empty its previous position
                    if object_dragging:
                        if current_object != 0:
                            object_dragging = False
                            if (x, y) in Game_move_logic.Possible_moves(current_object):
                                # Pawn Promotions - swaps promoted pawns model to queen
                                if current_object.model == Sprites.WP:
                                    if y == 0:
                                        print('White Promotion!')
                                        current_object.model = Sprites.WQ

                                    # Weird En passant shit
                                    elif (((x, y) == (current_object.row - 1, current_object.column - 1))
                                          or ((x, y) == (current_object.row + 1, current_object.column - 1))):
                                        if Game_move_logic.Castling_and_check_variables.last_moved_piece.row == x and Game_move_logic.Castling_and_check_variables.last_moved_piece.column == y + 1:
                                            print('EN PASSANT!')
                                            Game_move_logic.board[y + 1][x] = 0
                                            Update_board_state(Game_move_logic.board)

                                if current_object.model == Sprites.BP:
                                    if y == 7:
                                        print('Black Promotion!')
                                        current_object.model = Sprites.BQ

                                    # Weird En passant shit
                                    elif (((x, y) == (current_object.row - 1, current_object.column + 1))
                                          or ((x, y) == (current_object.row + 1, current_object.column + 1))):
                                        if Game_move_logic.Castling_and_check_variables.last_moved_piece != 0:
                                            if Game_move_logic.Castling_and_check_variables.last_moved_piece.row == x and Game_move_logic.Castling_and_check_variables.last_moved_piece.column == y - 1:
                                                print('EN PASSANT!')
                                                Game_move_logic.board[y - 1][x] = 0
                                                Update_board_state(Game_move_logic.board)

                                # Castling White
                                if current_object.model == Sprites.WK:
                                    if (x, y) == (2, 7) and Game_move_logic.Castling_and_check_variables.white_king_moved == 0 and Piece_Objects.Rook1 not in Game_move_logic.Castling_and_check_variables.rooks_moved:  # LONG
                                        Game_move_logic.board[7][2] = Piece_Objects.King1
                                        Game_move_logic.board[7][3] = Piece_Objects.Rook1
                                        Game_move_logic.board[7][4] = 0
                                        Game_move_logic.board[7][0] = 0
                                        Game_move_logic.Castling_and_check_variables.rooks_moved.append(Piece_Objects.Rook1)
                                        white_king_moved = 1

                                    elif (x, y) == (6, 7) and Game_move_logic.Castling_and_check_variables.white_king_moved == 0 and Piece_Objects.Rook2 not in Game_move_logic.Castling_and_check_variables.rooks_moved:  # SHORT
                                        Game_move_logic.board[7][6] = Piece_Objects.King1
                                        Game_move_logic.board[7][5] = Piece_Objects.Rook2
                                        Game_move_logic.board[7][4] = 0
                                        Game_move_logic.board[7][7] = 0
                                        Game_move_logic.Castling_and_check_variables.rooks_moved.append(Piece_Objects.Rook2)
                                        white_king_moved = 1

                                # Castling Black
                                if current_object.model == Sprites.BK:
                                    if (x, y) == (2, 0) and Game_move_logic.Castling_and_check_variables.black_king_moved == 0 and Piece_Objects.Rook3 not in Game_move_logic.Castling_and_check_variables.rooks_moved:  # LONG
                                        Game_move_logic.board[0][2] = Piece_Objects.King1
                                        Game_move_logic.board[0][3] = Piece_Objects.Rook3
                                        Game_move_logic.board[0][4] = 0
                                        Game_move_logic.board[0][0] = 0
                                        Game_move_logic.Castling_and_check_variables.rooks_moved.append(Piece_Objects.Rook3)
                                        black_king_moved = 1

                                    elif (x, y) == (6, 0) and Game_move_logic.Castling_and_check_variables.black_king_moved == 0 and Piece_Objects.Rook4 not in Game_move_logic.Castling_and_check_variables.rooks_moved:  # SHORT
                                        Game_move_logic.board[0][6] = Piece_Objects.King1
                                        Game_move_logic.board[0][5] = Piece_Objects.Rook4
                                        Game_move_logic.board[0][4] = 0
                                        Game_move_logic.board[0][7] = 0
                                        Game_move_logic.Castling_and_check_variables.rooks_moved.append(Piece_Objects.Rook4)
                                        black_king_moved = 1

                                # Remembers 1 turn back
                                previous_board = [[0 for i in range(8)]for j in range(8)]
                                for line in range(8):
                                    for p in range(8):
                                        previous_board[line][p] = Game_move_logic.board[line][p]

                                last_moved_piece = current_object
                                Game_move_logic.board[y][x] = current_object  # Copy the piece to move location
                                Game_move_logic.board[previous_column][previous_row] = 0  # Empty initial piece location

                                # Checks whether a move exposes allied king, if it does revert board state
                                if Game_move_logic.Friendly_Piece_Check(current_object.colour) == 0:
                                    Game_move_logic.board = previous_board
                                    current_turn = Game_move_logic.Swap_Turns(current_turn)

                                # If move succeeded all checks, update the board, zero the variables, swap turns
                                Update_board_state(Game_move_logic.board)
                                pygame.mixer.Sound.play(move_sound)
                                if Game_move_logic.Enemy_Piece_Check(current_object) == 1 and current_object.colour == Colour.BLACK:
                                    white_check = 1
                                    print("White Check")
                                elif Game_move_logic.Enemy_Piece_Check(current_object) == 1 and current_object.colour == Colour.WHITE:
                                    black_check = 1
                                    print("Black Check")
                                current_object = 0
                                previous_row = 0
                                previous_column = 0
                                current_turn = Game_move_logic.Swap_Turns(current_turn)

                                if Game_move_logic.Castling_and_check_variables.white_check == 1:
                                    if Game_move_logic.Checkmate_Check(Game_move_logic.board, Colour.WHITE) == 1:
                                        print("White Checkmate!")
                                        break
                                    else:
                                        print("No checkmate")
                                        white_check = 0
                                elif Game_move_logic.Castling_and_check_variables.black_check == 1:
                                    if Game_move_logic.Checkmate_Check(Game_move_logic.board, Colour.BLACK) == 1:
                                        print("Black Checkmate!")
                                        break
                                    else:
                                        print("No checkmate")
                                        black_check = 0

                            # Case if clicked cell is not possible for the piece to move to
                            else:
                                print('Disallowed move')
                                Update_board_state(Game_move_logic.board)
                                continue

                    else:  # If piece was clicked
                        if Game_move_logic.board[y][x] != 0:
                            if current_turn == Game_move_logic.board[y][x].colour:  # Check turn order
                                print(x, y)
                                object_dragging = True
                                current_object = Game_move_logic.board[y][x]  # store the piece clicked
                                previous_row = copy.deepcopy(current_object.row)
                                previous_column = copy.deepcopy(current_object.column)
                            else:
                                print('Current Turn = ' + str(current_turn))
                        else:
                            print(x, y)
# ----------------------------------------------------------------------------------------------------------------------
