# Handles user input and displaying current GameState object

import pygame as p

from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Initialize a global dictionary for images. Might give user option to their own chess set as the ones used in this
# project are not very high resolution
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


# Main driver for handling user input and updates graphics


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sq_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # mouse click location
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):  # User clicks source and destination is the same/ illegal move
                    sq_selected = ()  # Unselecting stored clicks and positions made by
                    player_clicks = []  # player during illegal move
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sq_selected = ()
                    player_clicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


# Draws squares and pieces on the board and responsible for all graphics on the board
def drawGameState(screen, gs):
    drawBoard(screen)  # draws squares on the board
    drawPieces(screen, gs.board)  # draws pieces on top of squares


# Draw squares on the board, top-left square always light
def drawBoard(screen):
    colors = [p.Color("light grey"), p.Color("dark grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
