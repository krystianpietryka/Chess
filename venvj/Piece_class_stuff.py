from enum import Enum
import pygame



class Colour(Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, column, row, model, colour):
        self.row = row
        self.column = column
        self.model = model
        self.colour = colour


# Load sprites into pygame
class Sprites:
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
class Piece_Objects:
    Pawn1 = Piece(6, 0, Sprites.WP, Colour.WHITE)
    Pawn2 = Piece(6, 1, Sprites.WP, Colour.WHITE)
    Pawn3 = Piece(6, 2, Sprites.WP, Colour.WHITE)
    Pawn4 = Piece(6, 3, Sprites.WP, Colour.WHITE)
    Pawn5 = Piece(6, 4, Sprites.WP, Colour.WHITE)
    Pawn6 = Piece(6, 5, Sprites.WP, Colour.WHITE)
    Pawn7 = Piece(6, 6, Sprites.WP, Colour.WHITE)
    Pawn8 = Piece(6, 7, Sprites.WP, Colour.WHITE)
    Pawn9 = Piece(1, 0, Sprites.BP, Colour.BLACK)
    Pawn10 = Piece(1, 1, Sprites.BP, Colour.BLACK)
    Pawn11 = Piece(1, 2, Sprites.BP, Colour.BLACK)
    Pawn12 = Piece(1, 3, Sprites.BP, Colour.BLACK)
    Pawn13 = Piece(1, 4, Sprites.BP, Colour.BLACK)
    Pawn14 = Piece(1, 5, Sprites.BP, Colour.BLACK)
    Pawn15 = Piece(1, 6, Sprites.BP, Colour.BLACK)
    Pawn16 = Piece(1, 7, Sprites.BP, Colour.BLACK)
    Knight1 = Piece(7, 1, Sprites.WH, Colour.WHITE)
    Knight2 = Piece(7, 6, Sprites.WH, Colour.WHITE)
    Knight3 = Piece(0, 1, Sprites.BH, Colour.BLACK)
    Knight4 = Piece(0, 6, Sprites.BH, Colour.BLACK)
    Rook1 = Piece(7, 0, Sprites.WR, Colour.WHITE)
    Rook2 = Piece(7, 7, Sprites.WR, Colour.WHITE)
    Rook3 = Piece(0, 0, Sprites.BR, Colour.BLACK)
    Rook4 = Piece(0, 7, Sprites.BR, Colour.BLACK)
    Bishop1 = Piece(7, 2, Sprites.WB, Colour.WHITE)
    Bishop2 = Piece(7, 5, Sprites.WB, Colour.WHITE)
    Bishop3 = Piece(0, 2, Sprites.BB, Colour.BLACK)
    Bishop4 = Piece(0, 5, Sprites.BB, Colour.BLACK)
    King1 = Piece(7, 4, Sprites.WK, Colour.WHITE)
    King2 = Piece(0, 4, Sprites.BK, Colour.BLACK)
    Queen1 = Piece(7, 3, Sprites.WQ, Colour.WHITE)
    Queen2 = Piece(0, 3, Sprites.BQ, Colour.BLACK)

