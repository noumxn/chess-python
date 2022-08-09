# Stores all info on current state of the game. Also determines what moves are valid in current position.
# Keeps move log.


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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 7, "b": 6, "c": 5, "d": 4,
                   "e": 3, "f": 2, "g": 1, "h": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __int__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
