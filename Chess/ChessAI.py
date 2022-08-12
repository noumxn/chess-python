import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def findBestMove(game_state, valid_moves):
    turn_multiplier = 1 if game_state.white_to_move else -1
    opp_min_max_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        game_state.makeMove(player_move)
        opp_moves = game_state.getValidMoves()
        if game_state.stale_mate:
            opp_max_score = STALEMATE
        elif game_state.check_mate:
            opp_max_score = -CHECKMATE
        else:
            opp_max_score = -CHECKMATE
            for opp_move in opp_moves:
                game_state.makeMove(opp_move)
                game_state.getValidMoves()
                if game_state.check_mate:
                    score = CHECKMATE
                elif game_state.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * scoreMaterial(game_state.board)
                if score > opp_max_score:
                    opp_max_score = score
                game_state.undoMove()
        if opp_max_score < opp_min_max_score:
            opp_min_max_score = opp_max_score
            best_player_move = player_move
        game_state.undoMove()
    return best_player_move


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score
