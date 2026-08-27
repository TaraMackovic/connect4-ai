import math 
import time

from game.board import create_board, print_board, get_legal_moves, make_move, copy_board
from game.rules import get_game_result
from search.heuristic_eval import evaluate 

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

def possible_states(state):
    for col in get_legal_moves(state.board):
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

def heuristic(state):
    return evaluate(state.board, player=1)


def minimize(state, depth):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return heuristic(state), state

    best_score = math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = maximize(next_state, depth - 1)
        if score < best_score:
            best_score = score
            best_state = next_state
    return best_score, best_state

def maximize(state, depth):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return heuristic(state), state
 
    best_score = -math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = minimize(next_state, depth - 1)
        if score > best_score:
            best_score = score
            best_state = next_state
    return best_score, best_state


# Minmax with alpha-beta pruning

def minimize_ab(state, depth, alpha=-math.inf, beta=math.inf):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return heuristic(state), state
 
    best_score = math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = maximize_ab(next_state, depth - 1, alpha, beta)
        if score < best_score:
            best_score = score
            best_state = next_state
        if best_score < beta:
            beta = best_score
        if alpha >= beta:
            return best_score, best_state
    return best_score, best_state
 
def maximize_ab(state, depth, alpha=-math.inf, beta=math.inf):
    if end(state):
        return evaluate_end(state), state
    if depth == 0:
        return heuristic(state), state
 
    best_score = -math.inf
    best_state = None
    for next_state in possible_states(state):
        score, _ = minimize_ab(next_state, depth - 1, alpha, beta)
        if score > best_score:
            best_score = score
            best_state = next_state
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            return best_score, best_state
    return best_score, best_state

if __name__ == "__main__":

    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 1, 2, 2, 2, 1, 0],
    ]
    state = State(board, curr_player=1)
    print_board(board)
    print("Igrac 1 (AI) bira kolonu (sa alpha-beta, depth = 5):")
 
    score, next_state = maximize_ab(state, depth=5)
    print(f"Predlozena kolona: {next_state.last_move}, score: {score}\n")
 
    print("Provjera na maloj dubini (depth = 1) - heuristika treba dati signal:")
    score_shallow, next_state_shallow = maximize_ab(State(board, curr_player=1), depth=1)
    print(f"Predlozena kolona (depth=1): {next_state_shallow.last_move}, score: {score_shallow}\n")
 
    # Poredjenje brzine Minmax bez alpha-beta i Minmax sa alpha-beta odsjecanjem
    print(f"{'Dubina':<8}{'Bez AB (s)':<14}{'Alpha-beta (s)':<16}{'Razlika':<8}")
    for depth in range(1, 5):
        t0 = time.time()
        maximize(State(board, curr_player=1), depth)
        t_mm = time.time() - t0
 
        t0 = time.time()
        maximize_ab(State(board, curr_player=1), depth)
        t_mmab = time.time() - t0
 
        difference = t_mm / t_mmab if t_mmab > 0 else float("inf")
        print(f"{depth:<8}{t_mm:<14.4f}{t_mmab:<16.4f}{difference:<8.2f}x")