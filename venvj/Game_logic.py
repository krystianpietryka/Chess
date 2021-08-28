import os, copy, pygame
from enum import Enum

# IMPORTANT!
# Pieces have row and column properties, but when calling board[][], all instances have swapped positions, like:
# Board[column][row] (because Board is a 2d table)

class Colour(Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, row, column, model, colour):
        self.row = row
        self.column = column
        self.model = model
        self.colour = colour


# Load sprites into pygame
board_image = pygame.image.load(r'Sprites/Board.png')
WB = pygame.image.load(r'Sprites/WB.png')
WH = pygame.image.load(r'Sprites/WH.png')
WP = pygame.image.load(r'Sprites/WP.png')
WR = pygame.image.load(r'Sprites/WR.png')
WQ = pygame.image.load(r'Sprites/WQ.png')
WK = pygame.image.load(r'Sprites/WK.png')
BB = pygame.image.load(r'Sprites/BB.png')
BH = pygame.image.load(r'Sprites/BH.png')
BP = pygame.image.load(r'Sprites/BP.png')
BR = pygame.image.load(r'Sprites/BR.png')
BQ = pygame.image.load(r'Sprites/BQ.png')
BK = pygame.image.load(r'Sprites/BK.png')
Red_cell = pygame.image.load(r'Sprites/Red_cell.png')

# Piece class Objects
Pawn1 = Piece(6, 0, WP, Colour.WHITE)
Pawn2 = Piece(6, 1, WP, Colour.WHITE)
Pawn3 = Piece(6, 2, WP, Colour.WHITE)
Pawn4 = Piece(6, 3, WP, Colour.WHITE)
Pawn5 = Piece(6, 4, WP, Colour.WHITE)
Pawn6 = Piece(6, 5, WP, Colour.WHITE)
Pawn7 = Piece(6, 6, WP, Colour.WHITE)
Pawn8 = Piece(6, 7, WP, Colour.WHITE)
Pawn9 = Piece(1, 0, BP, Colour.BLACK)
Pawn10 = Piece(1, 1, BP, Colour.BLACK)
Pawn11 = Piece(1, 2, BP, Colour.BLACK)
Pawn12 = Piece(1, 3, BP, Colour.BLACK)
Pawn13 = Piece(1, 4, BP, Colour.BLACK)
Pawn14 = Piece(1, 5, BP, Colour.BLACK)
Pawn15 = Piece(1, 6, BP, Colour.BLACK)
Pawn16 = Piece(1, 7, BP, Colour.BLACK)
Knight1 = Piece(7, 1, WH, Colour.WHITE)
Knight2 = Piece(7, 6, WH, Colour.WHITE)
Knight3 = Piece(0, 1, BH, Colour.BLACK)
Knight4 = Piece(0, 6, BH, Colour.BLACK)
Rook1 = Piece(7, 0, WR, Colour.WHITE)
Rook2 = Piece(7, 7, WR, Colour.WHITE)
Rook3 = Piece(0, 0, BR, Colour.BLACK)
Rook4 = Piece(0, 7, BR, Colour.BLACK)
Bishop1 = Piece(7, 2, WB, Colour.WHITE)
Bishop2 = Piece(7, 5, WB, Colour.WHITE)
Bishop3 = Piece(0, 2, BB, Colour.BLACK)
Bishop4 = Piece(0, 5, BB, Colour.BLACK)
King1 = Piece(7, 4, WK, Colour.WHITE)
King2 = Piece(0, 4, BK, Colour.BLACK)
Queen1 = Piece(7, 3, WQ, Colour.WHITE)
Queen2 = Piece(0, 3, BQ, Colour.BLACK)

# Starting board state
board = [[Rook3, Knight3, Bishop3, Queen2, King2, Bishop4, Knight4, Rook4],
         [Pawn9, Pawn10, Pawn11, Pawn12, Pawn13, Pawn14, Pawn15, Pawn16],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [Pawn1, Pawn2, Pawn3, Pawn4, Pawn5, Pawn6, Pawn7, Pawn8],
         [Rook1, Knight1, Bishop1, Queen1, King1, Bishop2, Knight2, Rook2]]


def Swap_Colour(p):
    if p.colour == Colour.WHITE:
        return Colour.BLACK
    else:
        return Colour.WHITE

def Swap_Turns(colour):
    if colour == Colour.WHITE:
        colour = Colour.BLACK
    else:
        colour = Colour.WHITE
    return colour


def Checkmate_Check(board, colour):
    count = 0
    amount_of_pieces = 0
    for l in board:
        for p in l:
            if p != 0 and p.colour == colour:
                amount_of_pieces += 1
                #print("count= ", count)
                if p.model != BK and p.model != WK:
                    if Friendly_Piece_Check(p) == 1:
                        count += 1
                else:
                    if not King_Check(Possible_moves(p), colour):
                        count += 1

    #print(count, amount_of_pieces)
    if count == amount_of_pieces:
        return 1
    else:
        return 0


# Checks if a friendly piece covers called piece
def Coverage(p):
    p.colour = Swap_Colour(p)   # Swap colour and call Possible moves, cheeky
    for l in board:
        for ally in l:
            if ally != 0 and ally.colour != p.colour:
                if (p.row, p.column) in Possible_moves(ally):
                    p.colour = Swap_Colour(p)
                    return 1
    p.colour = Swap_Colour(p)
    return 0

# Checks all opposite pieces on the board, compares their moves to potential king move,
# if they match, king move gets removed, because he would put himself in check
def King_Check(m, king_colour):
    moves = copy.deepcopy(m)
    for move in moves:
        for row in board:
            for p in row:
                if p != 0:
                    if p.colour != king_colour:
                        if p.model != WK and p.model != BK:
                            if p.model == BP or p.model == WP:  # Special case for pawns, we only check diagonals
                                if move == (p.row + 1, p.column - 1):
                                    while move in m:
                                        m.remove(move)
                                if move == (p.row - 1, p.column - 1):
                                    while move in m:
                                        m.remove(move)
                                if move == (p.row - 1, p.column + 1):
                                    while move in m:
                                        m.remove(move)
                                if move == (p.row + 1, p.column + 1):
                                    while move in m:
                                        m.remove(move)
                            else:   # Not a king and not a pawn
                                enemy_moves = Possible_moves(p)
                                if move in enemy_moves:
                                    if move in m:
                                        m.remove(move)
                        else:   # Case for enemy king
                            r = p.row
                            c = p.column
                            possible_enemy_king_moves = [(r+1, c+1), (r+1, c), (r, c+1), (r+1, c-1),
                                                         (r-1, c+1), (r-1, c-1), (r-1, c), (r, c-1)]
                            for enemy_move in possible_enemy_king_moves:
                                if move == enemy_move:
                                    if move in m:
                                        m.remove(move)
    moves = copy.deepcopy(m)
    for move in moves:
        if board[move[1]][move[0]] != 0:
            if Coverage(board[move[1]][move[0]]) == 1:
                m.remove(move)
    return m


# Checks if a piece move puts enemy king in check
def Enemy_Piece_Check(p):
    moves = Possible_moves(p)
    colour = p.colour
    for move in moves:
        if board[move[1]][move[0]] != 0:
            if (board[move[1]][move[0]].model == BK and colour == colour.WHITE) or (board[move[1]][move[0]].model == WK and colour == colour.BLACK):
                if colour == colour.WHITE:
                    return 1
                else:
                    return 1
    return 0


# Checks if a move exposes a king
def Friendly_Piece_Check(piece_colour):
        for l in board:
            for p in l:
                if p != 0 and p.colour != piece_colour:
                    moves = Possible_moves(p)
                    for move in moves:
                        if board[move[1]][move[0]] != 0:
                            if (board[move[1]][move[0]].model == BK and piece_colour == Colour.BLACK) or (board[move[1]][move[0]].model == WK and piece_colour == Colour.WHITE):
                                print("Move would expose the king")
                                return 0

        return 1


# DEBILU TRZEBA BYLO ROBIC TRY EXCEPTY ZAMIAST TYLU WARUNKOW NA GRANICACH PLANSZY
# Function returns all possible move locations for a given piece, including castling and en passant
def Possible_moves(piece):
    row = piece.row
    column = piece.column
    moves = []
    # White Pawn
    if piece.model == WP:
        if piece.column != 0:
            if piece.column == 6:  # pawn has not moved
                if board[5][piece.row] == 0:
                    if board[4][piece.row] == 0:  # 2 cells away free
                        moves.append((piece.row, 4))
                        moves.append((piece.row, 5))
                    else:
                        moves.append((piece.row, 5))
            else:  # pawn has moved and cell up is free
                if board[piece.column - 1][piece.row] == 0:
                    moves.append((piece.row, piece.column - 1))
            if piece.row != 7:  # Diagonal right
                if board[piece.column - 1][piece.row + 1] != 0:
                    if board[piece.column - 1][piece.row + 1].colour != piece.colour:
                        moves.append((piece.row + 1, piece.column - 1))
                if board[piece.column - 1][piece.row + 1] == 0 and board[piece.column][
                    piece.row + 1] == last_moved_piece:
                    if piece.column == 3:
                        moves.append((piece.row + 1, piece.column - 1))

            if piece.row != 0:  # Diagonal left
                if board[piece.column - 1][piece.row - 1] != 0:
                    if board[piece.column - 1][piece.row - 1].colour != piece.colour:
                        moves.append((piece.row - 1, piece.column - 1))
                # En passant
                if board[piece.column - 1][piece.row - 1] == 0 and board[piece.column][
                    piece.row - 1] == last_moved_piece:
                    if piece.column == 3:
                        moves.append((piece.row - 1, piece.column - 1))
        return moves

    # Black Pawn
    elif piece.model == BP:
        if piece.column != 7:
            if piece.column == 1:  # pawn has not moved (still in first row)
                if board[2][piece.row] == 0:
                    # 2 columns up free
                    if board[3][piece.row] == 0:
                        moves.append((piece.row, 2))
                        moves.append((piece.row, 3))
                    else:
                        moves.append((piece.row, 2))
            # pawn has moved and cell up is free
            else:
                if board[piece.column + 1][piece.row] == 0:
                    moves.append((piece.row, piece.column + 1))
            if piece.row != 7:  # Diagonal right
                if board[piece.column + 1][piece.row + 1] != 0:
                    if board[piece.column + 1][piece.row + 1].colour != piece.colour:
                        moves.append((piece.row + 1, piece.column + 1))
                if board[piece.column + 1][piece.row + 1] == 0 and board[piece.column][
                    piece.row + 1] == last_moved_piece:
                    if piece.column == 4:
                        moves.append((piece.row + 1, piece.column + 1))
            if piece.row != 0:  # Diagonal left
                if board[piece.column + 1][piece.row - 1] != 0:
                    if board[piece.column + 1][piece.row - 1].colour != piece.colour:
                        moves.append((piece.row - 1, piece.column + 1))
                # En passant
                if board[piece.column + 1][piece.row - 1] == 0 and board[piece.column][
                    piece.row - 1] == last_moved_piece:
                    if piece.column == 4:
                        moves.append((piece.row - 1, piece.column + 1))
        return moves

    # Knights
    elif piece.model == WH or piece.model == BH:
        if piece.row < 6:
            if piece.column != 7:
                if (board[piece.column + 1][piece.row + 2] == 0) or ((board[piece.column + 1][piece.row + 2] != 0)
                                                                     and board[piece.column + 1][
                                                                         piece.row + 2].colour != piece.colour):
                    moves.append((piece.row + 2, piece.column + 1))
            if piece.column != 0:
                if (board[piece.column - 1][piece.row + 2] == 0) or ((board[piece.column - 1][piece.row + 2] != 0)
                                                                     and board[piece.column - 1][
                                                                         piece.row + 2].colour != piece.colour):
                    moves.append((piece.row + 2, piece.column - 1))
        if piece.row > 1:
            if piece.column != 7:
                if (board[piece.column + 1][piece.row - 2] == 0) or ((board[piece.column + 1][piece.row - 2] != 0)
                                                                     and board[piece.column + 1][
                                                                         piece.row - 2].colour != piece.colour):
                    moves.append((piece.row - 2, piece.column + 1))
            if piece.column != 0:
                if (board[piece.column - 1][piece.row - 2] == 0) or ((board[piece.column - 1][piece.row - 2] != 0)
                                                                     and board[piece.column - 1][
                                                                         piece.row - 2].colour != piece.colour):
                    moves.append((piece.row - 2, piece.column - 1))
        if piece.column > 1:
            if piece.row != 0:
                if (board[piece.column - 2][piece.row - 1] == 0) or ((board[piece.column - 2][piece.row - 1] != 0)
                                                                     and board[piece.column - 2][
                                                                         piece.row - 1].colour != piece.colour):
                    moves.append((piece.row - 1, piece.column - 2))
            if piece.row != 7:
                if (board[piece.column - 2][piece.row + 1] == 0) or ((board[piece.column - 2][piece.row + 1] != 0)
                                                                     and board[piece.column - 2][
                                                                         piece.row + 1].colour != piece.colour):
                    moves.append((piece.row + 1, piece.column - 2))
        if piece.column < 6:
            if piece.row != 0:
                if (board[piece.column + 2][piece.row - 1] == 0) or ((board[piece.column + 2][piece.row - 1] != 0)
                                                                     and board[piece.column + 2][
                                                                         piece.row - 1].colour != piece.colour):
                    moves.append((piece.row - 1, piece.column + 2))
            if piece.row != 7:
                if (board[piece.column + 2][piece.row + 1] == 0) or ((board[piece.column + 2][piece.row + 1] != 0)
                                                                     and board[piece.column + 2][
                                                                         piece.row + 1].colour != piece.colour):
                    moves.append((piece.row + 1, piece.column + 2))
        return moves

    # Bishops
    elif piece.model == BB or piece.model == WB:
        # DR
        for i in range(1, min(8 - row, 8 - column)):
            if board[piece.column + i][piece.row + i] == 0:
                moves.append((piece.row + i, piece.column + i))
            else:
                if board[piece.column + i][piece.row + i].colour != piece.colour:
                    moves.append((piece.row + i, piece.column + i))
                break
        # DL
        for i in range(1, min(row + 1, 8 - column)):
            if board[piece.column + i][piece.row - i] == 0:
                moves.append((piece.row - i, piece.column + i))
            else:
                if board[piece.column + i][piece.row - i].colour != piece.colour:
                    moves.append((piece.row - i, piece.column + i))
                break
        # UL
        for i in range(1, min(row + 1, column + 1)):
            if board[piece.column - i][piece.row - i] == 0:
                moves.append((piece.row - i, piece.column - i))
            else:
                if board[piece.column - i][piece.row - i].colour != piece.colour:
                    moves.append((piece.row - i, piece.column - i))
                break
        # UR
        for i in range(1, min(8 - row, column + 1)):
            if board[piece.column - i][piece.row + i] == 0:
                moves.append((piece.row + i, piece.column - i))
            else:
                if board[piece.column - i][piece.row + i].colour != piece.colour:
                    moves.append((piece.row + i, piece.column - i))
                break

        return moves

    # Kings
    elif piece.model == BK or piece.model == WK:
        # Castling white
        if white_king_moved == 0 and piece.model == WK and piece.row == 4 and piece.column == 7:
            if (Rook1 not in rooks_moved) and board[7][3] == 0 and board[7][2] == 0 and board[7][1] == 0: # LONG
                castling_tiles = [(3,7), (2, 7), (1, 7)]
                castling_tiles = King_Check(castling_tiles, Colour.WHITE)
                if len(castling_tiles) == 3:
                    moves.append((2, 7))
            if (Rook2 not in rooks_moved) and board[7][5] == 0 and board[7][6] == 0:  # SHORT
                castling_tiles = [(5, 7), (6, 7)]
                castling_tiles = King_Check(castling_tiles, Colour.WHITE)
                if len(castling_tiles) == 2:
                    moves.append((6, 7))
        # Castling black
        if black_king_moved == 0 and piece.model == BK and piece.row == 4 and piece.column == 0:
            if (Rook3 not in rooks_moved) and board[0][3] == 0 and board[0][2] == 0 and board[0][1] == 0:  # LONG
                castling_tiles = [(3, 0), (2, 0), (1, 1)]
                castling_tiles = King_Check(castling_tiles, Colour.BLACK)
                if len(castling_tiles) == 3:
                    moves.append((2, 0))
            if (Rook4 not in rooks_moved) and board[0][5] == 0 and board[0][6] == 0:  # SHORT
                castling_tiles = [(5, 0), (6, 0)]
                castling_tiles = King_Check(castling_tiles, Colour.BLACK)
                if len(castling_tiles) == 2:
                    moves.append((6, 0))
        if piece.row != 7:
            if (board[piece.column][piece.row + 1] == 0) or ((board[piece.column][piece.row + 1] != 0)
                                                             and board[piece.column][
                                                                 piece.row + 1].colour != piece.colour):
                moves.append((piece.row + 1, piece.column))
            if piece.column != 0:
                if (board[piece.column - 1][piece.row + 1] == 0) or ((board[piece.column - 1][piece.row + 1] != 0)
                                                                     and board[piece.column - 1][
                                                                         piece.row + 1].colour != piece.colour):
                    moves.append((piece.row + 1, piece.column - 1))
            if piece.column != 7:
                if (board[piece.column + 1][piece.row + 1] == 0) or (
                        (board[piece.column + 1][piece.row + 1] != 0) and board[piece.column + 1]
                [piece.row + 1].colour != piece.colour):
                    moves.append((piece.row + 1, piece.column + 1))
        if piece.row != 0:
            if (board[piece.column][piece.row - 1] == 0) or (
                    (board[piece.column][piece.row - 1] != 0) and board[piece.column]
            [piece.row - 1].colour != piece.colour):
                moves.append((piece.row - 1, piece.column))
            if piece.column != 0:
                if (board[piece.column - 1][piece.row - 1] == 0) or (
                        (board[piece.column - 1][piece.row - 1] != 0) and board[piece.column - 1]
                [piece.row - 1].colour != piece.colour):
                    moves.append((piece.row - 1, piece.column - 1))
            if piece.column != 7:
                if (board[piece.column + 1][piece.row - 1] == 0) or (
                        (board[piece.column + 1][piece.row - 1] != 0) and board[piece.column + 1]
                [piece.row - 1].colour != piece.colour):
                    moves.append((piece.row - 1, piece.column + 1))
        if piece.column != 7:
            if (board[piece.column + 1][piece.row] == 0) or (
                    (board[piece.column + 1][piece.row] != 0) and board[piece.column + 1]
            [piece.row].colour != piece.colour):
                moves.append((piece.row, piece.column + 1))
        if piece.column != 0:
            if (board[piece.column - 1][piece.row] == 0) or (
                    (board[piece.column - 1][piece.row] != 0) and board[piece.column - 1]
            [piece.row].colour != piece.colour):
                moves.append((piece.row, piece.column - 1))

        return King_Check(moves, piece.colour)

    # Rooks
    elif piece.model == BR or piece.model == WR:
        # RIGHT
        for r in range(row + 1, 8):
            if board[column][r] != 0:
                if board[column][r].colour != piece.colour:
                    moves.append((r, column))
                break
            moves.append((r, column))
        # UP
        for c in range(column - 1, -1, -1):
            if board[c][row] != 0:
                if board[c][row].colour != piece.colour:
                    moves.append((row, c))
                break
            moves.append((row, c))
        # DOWN
        for c in range(column + 1, 8):
            if board[c][row] != 0:
                if board[c][row].colour != piece.colour:
                    moves.append((row, c))
                break
            moves.append((row, c))
        # LEFT
        for r in range(row - 1, -1, -1):
            if board[column][r] != 0:
                if board[column][r].colour != piece.colour:
                    moves.append((r, column))
                break
            moves.append((r, column))
        return moves

    # Queens
    elif piece.model == BQ or piece.model == WQ:
        # RIGHT
        for r in range(row + 1, 8):
            if board[column][r] != 0:
                if board[column][r].colour != piece.colour:
                    moves.append((r, column))
                break
            moves.append((r, column))
        # UP
        for c in range(column - 1, -1, -1):
            if board[c][row] != 0:
                if board[c][row].colour != piece.colour:
                    moves.append((row, c))
                break
            moves.append((row, c))
        # DOWN
        for c in range(column + 1, 8):
            if board[c][row] != 0:
                if board[c][row].colour != piece.colour:
                    moves.append((row, c))
                break
            moves.append((row, c))
        # LEFT
        for r in range(row - 1, -1, -1):
            if board[column][r] != 0:
                if board[column][r].colour != piece.colour:
                    moves.append((r, column))
                break
            moves.append((r, column))
        # DR
        for i in range(1, min(8 - row, 8 - column)):
            if board[piece.column + i][piece.row + i] == 0:
                moves.append((piece.row + i, piece.column + i))
            else:
                if board[piece.column + i][piece.row + i].colour != piece.colour:
                    moves.append((piece.row + i, piece.column + i))
                break
        # DL
        for i in range(1, min(row + 1, 8 - column)):
            if board[piece.column + i][piece.row - i] == 0:
                moves.append((piece.row - i, piece.column + i))
            else:
                if board[piece.column + i][piece.row - i].colour != piece.colour:
                    moves.append((piece.row - i, piece.column + i))
                break
        # UL
        for i in range(1, min(row + 1, column + 1)):
            if board[piece.column - i][piece.row - i] == 0:
                moves.append((piece.row - i, piece.column - i))
            else:
                if board[piece.column - i][piece.row - i].colour != piece.colour:
                    moves.append((piece.row - i, piece.column - i))
                break
        # UR
        for i in range(1, min(8 - row, column + 1)):
            if board[piece.column - i][piece.row + i] == 0:
                moves.append((piece.row + i, piece.column - i))
            else:
                if board[piece.column - i][piece.row + i].colour != piece.colour:
                    moves.append((piece.row + i, piece.column - i))
                break

        return moves

