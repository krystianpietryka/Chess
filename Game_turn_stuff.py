from Piece_class_stuff import Colour, Sprites


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
                if p.model != Sprites.BK and p.model != Sprites.WK:
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