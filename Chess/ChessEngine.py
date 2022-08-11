# Stores all info on current state of the game. Also determines what moves are valid in current position.
# Keeps move log.


class GameState:
    def __init__(self):
        # board is 8x8 2D list, each element is represented by two characters
        # 'w' or 'b' represents 'white' or 'black'
        # 'R', 'N', 'B', 'Q', 'K' and 'p' represent 'Rook', 'Knight', 'Bishop', 'Queen', 'King' and 'pawn' respectively
        # "--" represents empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = [7, 4]
        self.black_king_location = [0, 4]
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    def makeMove(self, move):
        """
        Takes a Move as a parameter and executes it.
        (this will not work for castling, pawn promotion and en-passant)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
        # en passant
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = '--'

        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        # castle move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # king-side castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]  # moves the rook to its new square
                self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
            else:  # queen-side castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]  # moves the rook to its new square
                self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook

        # update castling rights - whenever it is a rook or king move
        self.update_castle_rights(move)
        self.castle_rights_log.append(
            CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                         self.current_castling_rights.wqs, self.current_castling_rights.bqs))

    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            if move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # undo en passant
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col)
            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()
            # undo castle rights
            self.castle_rights_log.pop()  # get rid of the new castle rights from the move we are undoing
            newRights = self.castle_rights_log[-1]  # set the current castle rights to the last one in the list
            self.current_castling_rights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            # undo the castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king-side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:  # queen-side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

    def update_castle_rights(self, move):
        """
        Update the castle rights given the move
        """
        if move.piece_moved == 'wK':
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False

    def getValidMoves(self):
        # for log in self.castle_rights_log:
        #     print(log.wks, log.bks, log.wqs, log.bqs, end=". ")
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                          self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        moves = self.getAllPossibleMoves()

        if self.white_to_move:
            self.getCastleMoves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.getCastleMoves(self.black_king_location[0], self.black_king_location[1], moves)

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undoMove()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        """
        Determine if a current player is in check
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, col):
        """
        Determine if enemy can attack the square row col
        """
        self.white_to_move = not self.white_to_move  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  # square is under attack
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves

    def getPawnMoves(self, row, col, moves):
        if self.white_to_move:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_enpassant_move=True))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_enpassant_move=True))
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_enpassant_move=True))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_enpassant_move=True))

    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        # enemy_color = "b" if self.white_to_move else "w"
        if self.white_to_move:
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, row, col, moves):
        directions = ((-1, 1), (-1, -1), (1, 1), (1, -1))  # top-right, top-left, bottom-right, bottom-left
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, col, moves):
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + kingMoves[i][0]
            end_col = col + kingMoves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def getKnightMoves(self, row, col, moves):
        knight_moves = ((-2, 1), (-2, -1), (-1, -2), (1, -2), (2, 1), (2, -1), (1, 2), (-1, 2))
        ally_color = "w" if self.white_to_move else "b"
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def getCastleMoves(self, row, col, moves):
        """
        Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
        """
        if self.square_under_attack(row, col):
            return  # can't castle while in check
        if (self.white_to_move and self.current_castling_rights.wks) or (
                not self.white_to_move and self.current_castling_rights.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or (
                not self.white_to_move and self.current_castling_rights.bqs):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))

    def getQueensideCastleMoves(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is
    # corresponding to rows) and the second one being a letter between a-f (corresponding to columns), in order to
    # use this notation we need to map our [row][col] coordinates to match the ones used in the original chess game
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                self.piece_moved == "bp" and self.end_row == 7)
        # en passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        # castle move
        self.is_castle_move = is_castle_move

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)

    def getRankFile(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    # def getChessNotation(self):
    #     if self.is_pawn_promotion:
    #         return self.getRankFile(self.end_row, self.end_col) + "Q"
    #     if self.is_castle_move:
    #         if self.end_col == 1:
    #             return "0-0-0"
    #         else:
    #             return "0-0"
    #     if self.is_enpassant_move:
    #         return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
    #                                                                                             self.end_col) + " e.p."
    #     if self.piece_captured != "--":
    #         if self.piece_moved[1] == "p":
    #             return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
    #                                                                                                 self.end_col)
    #         else:
    #             return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col)
    #     else:
    #         if self.piece_moved[1] == "p":
    #             return self.getRankFile(self.end_row, self.end_col)
    #         else:
    #             return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col)
