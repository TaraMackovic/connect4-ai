# Benchmark: Heuristic vs Neural
# Mjerenje: 
# - broj pobjeda, 
# - prosjecno vrijeme po potezu,
# - dubina pretrage

# Heuristic-Agent vs Neural-Agent

import random
import time

from game.board import get_legal_moves
from game.rules import get_game_result
from search.minmax import State, maximize_ab, minimize_ab, clear_transposition_table
from search.heuristic_eval import evaluate as evaluate_heuristic
from neural.neural_eval import evaluate as evaluate_neural

HEURISTIC_PLAYER = 1
NEURAL_PLAYER = 2
DEPTH = 3
NUM_GAMES = 100
RANDOM_OPENING_MOVES = 2

def play_one_game(first_player, rand_opening_moves=RANDOM_OPENING_MOVES):

    clear_transposition_table()
    state = State(curr_player=first_player)
    move_count = 0

    heuristic_times = []
    neural_times = []

    while True:
        result = get_game_result(state.board)
        if result is not None:
            return result, move_count, heuristic_times, neural_times

        # Prvi potezi nausmicni (razbijanje determinizma)
        if move_count < rand_opening_moves:
            col = random.choice(get_legal_moves(state.board))
            state.play_move(col)
            move_count += 1
            continue

        if state.curr_player == HEURISTIC_PLAYER:
            start = time.perf_counter()
            _, next_state = maximize_ab(state, depth=DEPTH, eval_function=evaluate_heuristic)
            heuristic_times.append(time.perf_counter() - start)
        else:
            start = time.perf_counter()
            _, next_state = minimize_ab(state, depth=DEPTH, eval_function=evaluate_neural)
            neural_times.append(time.perf_counter() - start)


        if next_state is None:
            print("Greska: minmax nije vratio sledece stanje!")
            break

        state = next_state
        move_count += 1

def run_benchmark(num_games=NUM_GAMES):
    heuristic_wins = 0
    neural_wins = 0
    draws = 0

    move_counts = []
    all_heuristic_times = []
    all_neural_times = []

    for game_number in range(1, NUM_GAMES + 1):
        first_player = HEURISTIC_PLAYER if game_number % 2 == 1 else NEURAL_PLAYER

        result, move_count, heuristic_times, neural_times = play_one_game(first_player)

        if result == HEURISTIC_PLAYER:
            heuristic_wins += 1
        elif result == NEURAL_PLAYER:
            neural_wins += 1
        else:
            draws += 1

        move_counts.append(move_count)
        all_heuristic_times.extend(heuristic_times)
        all_neural_times.extend(neural_times)

        if game_number % 10 == 0:
            print(f"Odigrano {game_number}/{num_games} partija...")

    
    avg_moves = sum(move_counts) / len(move_counts)
    avg_heuristic_time = sum(all_heuristic_times) / len(all_heuristic_times) if all_heuristic_times else 0.0
    avg_neural_time = sum(all_neural_times) / len(all_neural_times) if all_neural_times else 0.0

    print("\n=== Rezultati benchmarka ===")
    print(f"Ukupno partija:            {num_games}")
    print(f"Heuristic pobjede:         {heuristic_wins} ({heuristic_wins/num_games*100:.1f}%)")
    print(f"Neural pobjede:            {neural_wins} ({neural_wins/num_games*100:.1f}%)")
    print(f"Nerijeseno:                {draws} ({draws/num_games*100:.1f}%)")
    print(f"Prosjecan broj poteza:     {avg_moves:.1f}")
    print(f"Vrijeme po potezu (Heuristic): {avg_heuristic_time*1000:.2f} ms")
    print(f"Vrijeme po potezu (Neural):    {avg_neural_time*1000:.2f} ms")

    return {
        "heuristic_wins": heuristic_wins,
        "neural_wins": neural_wins,
        "draws": draws,
        "avg_moves": avg_moves,
        "avg_heuristic_time": avg_heuristic_time,
        "avg_neural_time": avg_neural_time,
    }

if __name__ == "__main__":
    run_benchmark()
