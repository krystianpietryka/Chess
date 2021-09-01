from Game_move_logic import Possible_moves
import random
from Game_move_logic import board


def Random_Bot(b):
    available_moves = {}
    for line in b:
        for p in line:
            if p != 0:
                moves = Possible_moves(p)
                if not not moves:   # Dumbest boolean evaluation ever
                    available_moves[p] = moves[random.randint(0, len(moves)-1)]
    piece, coords = random.choice(list(available_moves.items()))
    move = (piece, coords)
    return move


print(Random_Bot(board))
