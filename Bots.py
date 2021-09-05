import random
from Game_move_logic import Possible_moves


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



