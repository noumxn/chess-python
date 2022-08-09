# Stores all info on current state of the game. Also determines what moves are valid in current position. Keeps move log.


class GameState:
    def __init__(self):
        # board is 8x8 2D list, each element is represented by two charecters
        # 'w' or 'b' represents 'white' or 'black'
        # 'R', 'N', 'B', 'Q', 'K' and 'p' represent 'Rook', 'Knight', 'Bishop', 'Queen', 'King' and 'pawn' respectively
        # "--" represents empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bK", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR"],
        ]

        self.whiteToMove = True
        self.moveLog = []
