from Piece_class_stuff import *
import copy


# IMPORTANT!
# Pieces have row and column properties, but when calling board[][], all instances have swapped positions, like:
# Board[column][row] (because Board is a 2d table)


# Variables used in castling and checks
class Castling_and_check_variables:
    rooks_moved = []
    black_king_moved = 0
    white_king_moved = 0
    white_check = 0
    black_check = 0
    last_moved_piece = 0


# Starting board state
board = [[Piece_Objects.Rook3, Piece_Objects.Knight3, Piece_Objects.Bishop3, Piece_Objects.Queen2, Piece_Objects.King2, Piece_Objects.Bishop4, Piece_Objects.Knight4, Piece_Objects.Rook4],
         [Piece_Objects.Pawn9, Piece_Objects.Pawn10, Piece_Objects.Pawn11, Piece_Objects.Pawn12, Piece_Objects.Pawn13, Piece_Objects.Pawn14, Piece_Objects.Pawn15, Piece_Objects.Pawn16],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [Piece_Objects.Pawn1, Piece_Objects.Pawn2, Piece_Objects.Pawn3, Piece_Objects.Pawn4, Piece_Objects.Pawn5, Piece_Objects.Pawn6, Piece_Objects.Pawn7, Piece_Objects.Pawn8],
         [Piece_Objects.Rook1, Piece_Objects.Knight1, Piece_Objects.Bishop1, Piece_Objects.Queen1, Piece_Objects.King1, Piece_Objects.Bishop2, Piece_Objects.Knight2, Piece_Objects.Rook2]]


# Checks if a friendly piece covers called piece
def Coverage(p):
    p.colour = Swap_Colour(p)   # Swap colour and call Possible moves, cheeky
    for line in board:
        for ally in line:
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
                        if p.model != Sprites.WK and p.model != Sprites.BK:
                            if p.model == Sprites.BP or p.model == Sprites.WP:  # Special pawn case, check diagonals
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
            if (board[move[1]][move[0]].model == Sprites.BK and colour == colour.WHITE) or (board[move[1]][move[0]].model == Sprites.WK and colour == colour.BLACK):
                if colour == colour.WHITE:
                    return 1
                else:
                    return 1
    return 0


# Checks if a move exposes a king
def Friendly_Piece_Check(piece_colour):
    for line in board:
        for p in line:
            if p != 0 and p.colour != piece_colour:
                moves = Possible_moves(p)
                for move in moves:
                    if board[move[1]][move[0]] != 0:
                        if (board[move[1]][move[0]].model == Sprites.BK) or (board[move[1]][move[0]].model == Sprites.WK):
                            print("Move would expose the king")
                            return 0

    return 1


# Function returns all possible move locations for a given piece, including castling and en passant
def Possible_moves(piece):
    row = piece.row
    column = piece.column
    moves = []
    # White Pawn
    if piece.model == Sprites.WP:
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
                    piece.row + 1] == Castling_and_check_variables.last_moved_piece:
                    if piece.column == 3:
                        moves.append((piece.row + 1, piece.column - 1))

            if piece.row != 0:  # Diagonal left
                if board[piece.column - 1][piece.row - 1] != 0:
                    if board[piece.column - 1][piece.row - 1].colour != piece.colour:
                        moves.append((piece.row - 1, piece.column - 1))
                # En passant
                if board[piece.column - 1][piece.row - 1] == 0 and board[piece.column][
                    piece.row - 1] == Castling_and_check_variables.last_moved_piece:
                    if piece.column == 3:
                        moves.append((piece.row - 1, piece.column - 1))
        return moves

    # Black Pawn
    elif piece.model == Sprites.BP:
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
                    piece.row + 1] == Castling_and_check_variables.last_moved_piece:
                    if piece.column == 4:
                        moves.append((piece.row + 1, piece.column + 1))
            if piece.row != 0:  # Diagonal left
                if board[piece.column + 1][piece.row - 1] != 0:
                    if board[piece.column + 1][piece.row - 1].colour != piece.colour:
                        moves.append((piece.row - 1, piece.column + 1))
                # En passant
                if board[piece.column + 1][piece.row - 1] == 0 and board[piece.column][
                    piece.row - 1] == Castling_and_check_variables.last_moved_piece:
                    if piece.column == 4:
                        moves.append((piece.row - 1, piece.column + 1))
        return moves

    # Knights
    elif piece.model == Sprites.WH or piece.model == Sprites.BH:
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
    elif piece.model == Sprites.BB or piece.model == Sprites.WB:
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
    elif piece.model == Sprites.BK or piece.model == Sprites.WK:
        # Castling white
        if Castling_and_check_variables.white_king_moved == 0 and piece.model == Sprites.WK and piece.row == 4 and piece.column == 7:
            if (Piece_Objects.Rook1 not in Castling_and_check_variables.rooks_moved) and board[7][3] == 0 and board[7][2] == 0 and board[7][1] == 0:    # LONG
                castling_tiles = [(3, 7), (2, 7), (1, 7)]
                castling_tiles = King_Check(castling_tiles, Colour.WHITE)
                if len(castling_tiles) == 3:
                    moves.append((2, 7))
            if (Piece_Objects.Rook2 not in Castling_and_check_variables.rooks_moved) and board[7][5] == 0 and board[7][6] == 0:  # SHORT
                castling_tiles = [(5, 7), (6, 7)]
                castling_tiles = King_Check(castling_tiles, Colour.WHITE)
                if len(castling_tiles) == 2:
                    moves.append((6, 7))
        # Castling black
        if Castling_and_check_variables.black_king_moved == 0 and piece.model == Sprites.BK and piece.row == 4 and piece.column == 0:
            if (Piece_Objects.Rook3 not in Castling_and_check_variables.rooks_moved) and board[0][3] == 0 and board[0][2] == 0 and board[0][1] == 0:  # LONG
                castling_tiles = [(3, 0), (2, 0), (1, 1)]
                castling_tiles = King_Check(castling_tiles, Colour.BLACK)
                if len(castling_tiles) == 3:
                    moves.append((2, 0))
            if (Piece_Objects.Rook4 not in Castling_and_check_variables.rooks_moved) and board[0][5] == 0 and board[0][6] == 0:  # SHORT
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
    elif piece.model == Sprites.BR or piece.model == Sprites.WR:
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
    elif piece.model == Sprites.BQ or piece.model == Sprites.WQ:
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
    for line in board:
        for p in line:
            if p != 0 and p.colour == colour:
                amount_of_pieces += 1
                if p.model != Sprites.BK and p.model != Sprites.WK:
                    if Friendly_Piece_Check(p) == 1:
                        count += 1
                else:
                    if not King_Check(Possible_moves(p), colour):
                        count += 1
    if count == amount_of_pieces:
        return 1
    else:
        return 0
