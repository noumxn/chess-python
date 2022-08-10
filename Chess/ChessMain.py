# Handles user input and displaying current GameState object

import pygame as p
import ChessEngine

BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# Initialize a global dictionary for images. Might give user option to their own chess set as the ones used in this
# project are not very high resolution
def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


# Main driver for handling user input and updates graphics


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user
    player_clicks = []  # this will keep track of player clicks (two tuples)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                # p.quit()
                # sys.exit()
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                    square_selected = ()  # deselect
                    player_clicks = []  # clear clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)  # append for both 1st and 2nd click
                if len(player_clicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.getChessNotation())
                    if move in valid_moves:
                        game_state.makeMove(move)
                        move_made = True
                        square_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [square_selected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game_state.undoMove()
                    move_made = True

        if move_made:
            valid_moves = game_state.getValidMoves()
            move_made = False

        drawGameState(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


# Draws squares and pieces on the board and responsible for all graphics on the board

def drawGameState(screen, game_state):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


# Draw squares on the board, top-left square always light
def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("light grey"), p.Color("dark grey")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == "__main__":
    main()
