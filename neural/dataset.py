"""
Generisanje trening podataka za neuronsku mrezu

Faza 1: nasumicne partije, bez pravih labela (placeholder)
Faza 2: zamijena radnom poteza minmax potezima i labelirati pozicije minmax evaluacijom

"""
import random

# Funkcija za simulaciju partije random potezima
def generate_random_game(rows=6, cols=7):
    """
    TODO: zamijeniti rucnu logiku pozivima na prave funkcije iz board.py

    """

    board = [0] * (rows*cols) # placeholder reprezentacija
    history = []
    current_player = 1

    for _ in range(rows * cols):
        # placeholder top red provjera 
        legal_cols = [c for c in range(cols) if board[c] == 0]
        if not legal_cols:
            break
        move = random.choice(legal_cols)
    
        history.append((board.copy(), move, current_player))

        # placeholder "drop piece" logika (pronalazenje prvog slobodnog reda u koloni move)

        # switch igraca
        current_player = 2 if current_player == 1 else 1

    return history

# Funkcija za generisanje dataset-a od num_games nasumicnih partija
def generate_dataset(num_games=1000):
    """
    TODO: dodati labeliranje (minmax eval)
    """
    dataset = []
    for _ in range(num_games):
        game_history = generate_random_game()
        print(game_history)
        dataset.extend(game_history)
    return dataset

if __name__ == "__main__":
    data = generate_dataset(num_games=10)
    print(f"Generisano {len(data)} pozicija iz 10 partija  (placeholder, bez labela)")
