# Generisanje trening podataka za neuronsku mrezu

import math
import random
import pickle
import os

from game.board import create_board, make_move, is_valid_move, copy_board, get_legal_moves
from game.rules import get_game_result

from search.minmax import State, maximize_ab, minimize_ab, clear_transposition_table
from search.heuristic_eval import evaluate as evaluate_heuristic

DEPTH = 3
EPSILON = 0.3 # vjerovatnoca random poteza 
ALPHA = 0.7 # tezinski koeficijent
NORM = 200.0

def scale_score(raw_score, norm=NORM, win_threshold=50000):
    if raw_score >= win_threshold:
        return 1.0
    elif raw_score <= -win_threshold:
        return -1.0
    else:
        return math.tanh(raw_score / norm)

def label_from_outcome(result, player):
    if result == "draw":
        return 0.0
    return 1.0 if result == player else -1.0

def generate_selfplay_game(depth=DEPTH, epsilon=EPSILON):
    clear_transposition_table()
    state = State(curr_player=1)
    positions = []

    while True:
        result = get_game_result(state.board)
        if result is not None:
            return positions, result
        
        # snapshot prije poteza
        board_snapshot = copy_board(state.board)
        positions.append((board_snapshot, state.curr_player))

        legal_moves = get_legal_moves(state.board)

        if random.random() < epsilon:
            col = random.choice(legal_moves)
            state.play_move(col)
        else:
            if state.curr_player == 1:
                _, next_state = maximize_ab(state, depth=depth, eval_function=evaluate_heuristic)
            else:
                _, next_state = minimize_ab(state, depth=depth, eval_function=evaluate_heuristic)

            if next_state is None:
                # ako minmax ne vrati stanje
                col = random.choice(legal_moves)
                state.play_move(col)
            else:
                state = next_state


def minimax_score(board_snapshot, player, depth=DEPTH):
    state = State(copy_board(board_snapshot), curr_player=player)
    if player == 1:
        score_p1, _ = maximize_ab(state, depth=depth, eval_function=evaluate_heuristic)
    else:
        score_p1, _ = minimize_ab(state, depth=depth, eval_function=evaluate_heuristic)

    return score_p1 if player == 1 else -score_p1


# Funkcija za generisanje dataset-a kao listu (board, player, label) trojki (Outcome-based pristup)
def generate_dataset_ob(num_games=1000, depth=DEPTH, epsilon=EPSILON, save_path=None):
    dataset = []
    for i in range(num_games):
        positions, result = generate_selfplay_game(depth=depth, epsilon=epsilon)
        for board_snapshot, player in positions:
            dataset.append((board_snapshot, player, label_from_outcome(result, player)))

        if (i + 1) % 100 == 0:
            print(f"Odigrano {i + 1}/{num_games} partija...")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            pickle.dump(dataset, f)
        print(f"Dataset sacuvan: {save_path} ({len(dataset)} pozicija)")
        
    return dataset

def combined_label(minimax_score, outcome_label, alpha=ALPHA):
    return alpha * minimax_score + (1-alpha) * outcome_label

def generate_dataset_hybrid(num_games=1000, depth=DEPTH, epsilon=EPSILON, alpha=ALPHA, norm=NORM, save_path=None):
    dataset = []

    for i in range(num_games):
        positions, result = generate_selfplay_game(depth=depth, epsilon=epsilon)

        for board_snapshot, player in positions:
            raw_score = minimax_score(board_snapshot, player, depth=depth)

            scaled = scale_score(raw_score, norm=norm)

            outcome_label = label_from_outcome(result, player)
            final_label = combined_label(scaled, outcome_label, alpha=alpha)
            
            dataset.append((board_snapshot, player, final_label))

        if (i + 1) % 100 == 0:
            print(f"Odigrano {i+1}/{num_games} partija...")

    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            pickle.dump(dataset, f)
        print(f"Dataset sacuvan: {save_path} ({len(dataset)} pozicija)")

    return dataset

def load_dataset(path):
    with open(path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    #data_outcome_based = generate_dataset_ob(num_games=3000, save_path="data/dataset_outcome_based.pkl")
    #print(f"Generisano {len(data_outcome_based)} pozicija")
    
    data_hybrid = generate_dataset_hybrid(num_games=3000, save_path="data/dataset_hybrid.pkl")
    #print(f"Generisano {len(data_hybrid)} pozicija")
    #print("Primjer pozicije (board, player, label):")
    #print(data_hybrid[0])
    
