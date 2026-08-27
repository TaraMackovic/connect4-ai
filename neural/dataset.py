"""
Generisanje trening podataka za neuronsku mrezu

Faza 1: nasumicne partije, bez pravih labela (placeholder)
Faza 2: zamijena radnom poteza minmax potezima i labelirati pozicije minmax evaluacijom

"""
import random
import pickle

from game.board import create_board, make_move, is_valid_move, copy_board, get_legal_moves
from game.rules import get_game_result

# Funkcija za simulaciju partije random potezima koristeci board.py/rules.py funkcije
def generate_random_game(rows=6, cols=7):
    board = create_board()
    positions = []
    current_player = 1

    while True:
        legal_moves = get_legal_moves(board)

        if not legal_moves:
            return positions, get_game_result(board) # draw

        # snapshot prije poteza
        board_snapshot = copy_board(board)
        positions.append((board_snapshot, current_player))

        col = random.choice(legal_moves)
        make_move(board, col, current_player)

        results = get_game_result(board)
        if results is not None:
            return positions, results

        current_player = 2 if current_player == 1 else 1

# TODO (Faza 2): label_from_outcome trenutno dodjeljuje ishod cijele partije
# svakoj poziciji (i ranim i kasnim potezima) - gruba aproksimacija.
# Zamijeniti minimax evaluacijom same pozicije.
def label_from_outcome(result, player):
    if result == "draw":
        return 0.0
    return 1.0 if result == player else -1.0

# Funkcija za generisanje dataset-a kao listu (board, player, label) trojki (Monte Carlo pristup)
def generate_dataset(num_games=1000, save_path=None):
    """
    TODO: dodati labeliranje (minmax eval)
    """
    dataset = []
    for i in range(num_games):
        positions, result = generate_random_game()
        for board_snapshot, player in positions:
            dataset.append((board_snapshot, player, label_from_outcome(result, player)))

        if (i + 1) % 100 == 0:
            print(f"Odigrano {i + 1}/{num_games} partija...")

    if save_path:
        with open(save_path, "wb") as f:
            pickle.dump(dataset, f)
        print(f"Dataset sacuvan: {save_path} ({len(dataset)} pozicija)")
        
    return dataset

def analyze_outcomes(num_games=1000):
    p1, p2, draws = 0, 0, 0

    for _ in range(num_games):
        _, result = generate_random_game()
        if result == 1:
            p1 += 1
        elif result == 2:
            p2 += 1
        elif result == "draw":
            draws += 1

    print(f"Stistika: za {num_games} igara: ")
    print(f"Pobjede igraca 1: {(p1/num_games)*100:.1f}%")
    print(f"Pobjede igraca 2: {(p2/num_games)*100:.1f}%")
    print(f"Draw: {(draws/num_games)*100:.1f}%")

def load_dataset(path):
    with open(path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    data = generate_dataset(num_games=2000, save_path="data/random_games.pkl")
    print(f"Generisano {len(data)} pozicija iz 2000 partija")
    print("Primjer pozicije (board, player, label)")
    print(data[0])

    #analyze_outcomes()
