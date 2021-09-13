import random
from Game_move_logic import Possible_moves
from Piece_class_stuff import Sprites, Colour


def Bot_Choice(number, b, colour):
    if number == 1:
        move = Random_Bot(b, colour)
        return move


def Random_Bot(b, colour):
    available_moves = {}
    for line in b:
        for p in line:
            if p != 0 and p.colour == colour:
                moves = Possible_moves(p)
                if not not moves:   # Dumbest boolean evaluation ever
                    available_moves[p] = moves[random.randint(0, len(moves)-1)]
    piece, coords = random.choice(list(available_moves.items()))
    move = (piece, coords)
    return move


# Evaluates board score (Used in MiniMax algorithm)
def Shannon_Evaluation(board):
    score = 0
    for line in board:
        for p in line:
            if p != 0:
                if p.model == Sprites.WP:
                    score -= Doubled_Pawns(board, p)
                    score -= Blocked_Pawns(board, p)
                    score -= Isolated_Pawns(board, p)
                    score += 1
                elif p.model == Sprites.BP:
                    score += Doubled_Pawns(board, p)
                    score += Blocked_Pawns(board, p)
                    score += Isolated_Pawns(board, p)
                    score -= 1
                elif p.model == Sprites.WB:
                    score += 3
                elif p.model == Sprites.BB:
                    score -= 3
                elif p.model == Sprites.WH:
                    score += 3
                elif p.model == Sprites.BH:
                    score -= 3
                elif p.model == Sprites.WR:
                    score += 5
                elif p.model == Sprites.BR:
                    score -= 5
                elif p.model == Sprites.WQ:
                    score += 9
                elif p.model == Sprites.BQ:
                    score -= 9
                elif p.model == Sprites.WK:
                    score += 200
                elif p.model == Sprites.BK:
                    score -= 200
    score += Mobility(board)
    score = round(score, 1)
    return score


# Checks if a piece blocks pawns advance
def Blocked_Pawns(board, pawn):
    if pawn.colour == Colour.WHITE:
        if board[pawn.column-1][pawn.row] != 0:
            return 0.5
        return 0
    else:
        if board[pawn.column + 1][pawn.row] != 0:
            return 0.5
        return 0


# Checks if a pawn is not in a pawn chain (no adjacent pawns of the same colour)
# !DOES NOT WORK CURRENTLY
def Isolated_Pawns(board, pawn):
    for column in range(-1, 2, 1):
        for row in range(-1, 2, 1):
            if pawn.column + column != pawn.column and pawn.row + row != pawn.row:
                try:
                    if board[pawn.column + column][pawn.row + row] != 0:
                        if board[pawn.column + column][pawn.row + row].model == pawn.model:
                            return 0
                except IndexError:
                    pass
    return 0.5


# Checks if a pawn blocks a pawn
def Doubled_Pawns(board, pawn):
    if pawn.colour == Colour.WHITE:
        if board[pawn.column - 1][pawn.row] != 0 and board[pawn.column - 1][pawn.row].model == Sprites.WP:
            return 0.5
        return 0
    else:
        if board[pawn.column + 1][pawn.row] != 0 and board[pawn.column + 1][pawn.row].model == Sprites.BP:
            return 0.5
        return 0


# Count the amount of possible moves for a given piece colour
def Mobility(board):
    score = 0
    for line in board:
        for piece in line:
            if piece != 0:
                moves = Possible_moves(piece)
                if piece.colour == Colour.WHITE:
                    score += (len(moves) * 0.1)    # Every possible move is worth 0,1 score
                else:
                    score -= (len(moves) * 0.1)
    return score
