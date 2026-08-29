import math 

from game.board import create_board, get_legal_moves, make_move, copy_board
from game.rules import get_game_result

class State:
    def __init__(self, board=None, curr_player=1):
        self.board = board if board is not None else create_board()
        self.curr_player = curr_player
        self.last_move = None
        self.move_count = 0
 
    def play_move(self, col):
        make_move(self.board, col, self.curr_player)
        self.last_move = col
        self.curr_player = 2 if self.curr_player == 1 else 1
        self.move_count += 1

def end(state):
    return get_game_result(state.board) is not None


def ordered_columns(board):
    center = len(board[0]) // 2
    moves = get_legal_moves(board)
    return sorted(moves, key=lambda col: abs(col-center))

def possible_states(state):
    for col in ordered_columns(state.board):
        next_state = State(copy_board(state.board), state.curr_player)
        next_state.move_count = state.move_count
        next_state.play_move(col)
        yield next_state

def evaluate_end(state):
    result = get_game_result(state.board)
    if result == 1:
        return math.inf
    if result == 2:
        return -math.inf
    return 0  # draw

def evaluate_state(state, eval_function):
    return eval_function(state.board, player=1)

def minimize(state, depth, eval_function):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return evaluate_state(state, eval_function), state

    best_score = math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = maximize(next_state, depth - 1, eval_function)
        if best_state is None or score < best_score:
            best_score = score
            best_state = next_state
    return best_score, best_state

def maximize(state, depth, eval_function):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return evaluate_state(state, eval_function), state
 
    best_score = -math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = minimize(next_state, depth - 1, eval_function)
        if best_state is None or score > best_score:
            best_score = score
            best_state = next_state
    return best_score, best_state

transposition_table = {}

def board_key(board):
    return tuple(tuple(row) for row in board)

def clear_transposition_table():
    transposition_table.clear()

# Minmax with alpha-beta pruning

def minimize_ab(state, depth, eval_function, alpha=-math.inf, beta=math.inf, use_tt=True):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return evaluate_state(state, eval_function), state

    key = (board_key(state.board), depth, id(eval_function))
    if use_tt and key in transposition_table:
        return transposition_table[key]
 
    best_score = math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = maximize_ab(next_state, depth - 1, eval_function, alpha, beta, use_tt)
        if best_state is None or score < best_score:
            best_score = score
            best_state = next_state
        if best_score < beta:
            beta = best_score
        if alpha >= beta:
            break

    if use_tt:
        transposition_table[key] = (best_score, best_state)
    return best_score, best_state
 
def maximize_ab(state, depth, eval_function, alpha=-math.inf, beta=math.inf, use_tt=True):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return evaluate_state(state, eval_function), state

    key = (board_key(state.board), depth, id(eval_function))
    if use_tt and key in transposition_table:
        return transposition_table[key]
 
    best_score = -math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = minimize_ab(next_state, depth - 1, eval_function, alpha, beta, use_tt)
        if best_state is None or score > best_score:
            best_score = score
            best_state = next_state
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break

    if use_tt:
        transposition_table[key] = (best_score, best_state)
    return best_score, best_state