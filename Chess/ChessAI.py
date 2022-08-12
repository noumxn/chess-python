import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 1


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


def findBestMoveMinMax(game_state, valid_moves):
    global next_move
    next_move = None
    findMoveMinMax(game_state, valid_moves, DEPTH, game_state.white_to_move)
    return next_move


def findMoveMinMax(game_state, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return scoreMaterial(game_state.board)

    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
        return min_score


# +ve score better for white, -ve score better from black
def scoreBoard(game_state):
    if game_state.check_mate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stale_mate:
        return STALEMATE
    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score
