# Testiranje razlicitih dubina pretrage

import random
import time
import os

from game.board import get_legal_moves
from game.rules import get_game_result
from search.minmax import State, maximize_ab, minimize_ab, clear_transposition_table
from search.heuristic_eval import evaluate as evaluate_heuristic
from neural.neural_eval import evaluate as evaluate_neural

HEURISTIC_PLAYER = 1
NEURAL_PLAYER = 2
DEPTHS = [1, 2, 3, 4]
NUM_GAMES = 100
RANDOM_OPENING_MOVES = 2

def play_one_game(depth, first_player, rand_opening_moves=RANDOM_OPENING_MOVES):
    state = State(curr_player=first_player)
    move_count = 0

    heuristic_times = []
    neural_times = []

    clear_transposition_table()

    while True:
        result = get_game_result(state.board)

        if result is not None:
            return result, move_count, heuristic_times, neural_times

        if move_count < rand_opening_moves:
            col = random.choice(get_legal_moves(state.board))
            state.play_move(col)
            move_count += 1
            continue


        if state.curr_player == HEURISTIC_PLAYER:
            start = time.perf_counter()
            _, next_state = maximize_ab(state, depth=depth, eval_function=evaluate_heuristic)
            heuristic_times.append(time.perf_counter() - start)
        else:
            start = time.perf_counter()
            _, next_state = minimize_ab(state, depth=depth, eval_function=evaluate_neural)
            neural_times.append(time.perf_counter() - start)


        if next_state is None:
            print("Greska: minmax nije vratio sledece stanje!")
            break

        state = next_state
        move_count += 1


def run_depth_test(depth, num_games=NUM_GAMES):
    heuristic_wins = 0
    neural_wins = 0
    draws = 0

    move_counts = []
    all_heuristic_times = []
    all_neural_times = []

    for game_number in range(1, num_games + 1):
        first_player = HEURISTIC_PLAYER if game_number % 2 == 1 else NEURAL_PLAYER

        result, move_count, heuristic_times, neural_times = play_one_game(depth=depth, first_player=first_player)

        if result == HEURISTIC_PLAYER:
            heuristic_wins += 1
        elif result == NEURAL_PLAYER:
            neural_wins += 1
        else:
            draws += 1

        move_counts.append(move_count)
        all_heuristic_times.extend(heuristic_times)
        all_neural_times.extend(neural_times)

    avg_moves = sum(move_counts) / len(move_counts)
    avg_heuristic_time = (sum(all_heuristic_times) / len(all_heuristic_times) if all_heuristic_times else 0.0)
    avg_neural_time = (sum(all_neural_times) / len(all_neural_times) if all_neural_times else 0.0)

    return {
        "depth": depth,
        "heuristic_wins": heuristic_wins,
        "neural_wins": neural_wins,
        "draws": draws,
        "avg_moves": avg_moves,
        "avg_heuristic_time": avg_heuristic_time,
        "avg_neural_time": avg_neural_time,
    }


def run_all_depths(depths=DEPTHS, num_games=NUM_GAMES, save_path=None):
    results = []

    print("=== Test dubina pretrage ===")
    print(f"Broj partija po dubini: {num_games}")
    print(f"Dubine: {', '.join(map(str, depths))}")

    for depth in depths:
        print(f"\nTestiranje DEPTH = {depth}")
        result = run_depth_test(depth=depth, num_games=num_games)
        results.append(result)

        print(f"Heuristic: {result['heuristic_wins']} pobjeda "
              f"({result['heuristic_wins'] / num_games * 100:.1f}%)")
        print(f"Neural:    {result['neural_wins']} pobjeda "
              f"({result['neural_wins'] / num_games * 100:.1f}%)")
        print(f"Nerijeseno: {result['draws']} "
              f"({result['draws'] / num_games * 100:.1f}%)")
        print(f"Prosjecan broj poteza: {result['avg_moves']:.1f}")
        print(f"Prosjecno vrijeme Heuristic: "
              f"{result['avg_heuristic_time'] * 1000:.2f} ms")
        print(f"Prosjecno vrijeme Neural:    "
              f"{result['avg_neural_time'] * 1000:.2f} ms")

    print("\n=== Pregled rezultata ===")
    print(
        f"{'Depth':<8}"
        f"{'Heur. wins':<14}"
        f"{'Neural wins':<14}"
        f"{'Draws':<10}"
        f"{'Avg moves':<12}"
        f"{'Heur. ms':<12}"
        f"{'Neural ms':<12}"
    )
    print("-" * 82)

    for result in results:
        print(
            f"{result['depth']:<8}"
            f"{result['heuristic_wins']:<14}"
            f"{result['neural_wins']:<14}"
            f"{result['draws']:<10}"
            f"{result['avg_moves']:<12.1f}"
            f"{result['avg_heuristic_time'] * 1000:<12.2f}"
            f"{result['avg_neural_time'] * 1000:<12.2f}"
        )

    if save_path:
        directory = os.path.dirname(save_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(save_path, "a", encoding="utf-8") as f:
            f.write("=== Rezultati testa dubina pretrage ===\n")
            f.write(f"Broj partija po dubini: {num_games}\n")
            f.write(f"Dubine: {', '.join(map(str, depths))}\n\n")

            for result in results:
                f.write(f"DEPTH = {result['depth']}\n")
                f.write(
                    f"Heuristic: {result['heuristic_wins']} pobjeda "
                    f"({result['heuristic_wins'] / num_games * 100:.1f}%)\n"
                )
                f.write(
                    f"Neural:    {result['neural_wins']} pobjeda "
                    f"({result['neural_wins'] / num_games * 100:.1f}%)\n"
                )
                f.write(
                    f"Nerijeseno: {result['draws']} "
                    f"({result['draws'] / num_games * 100:.1f}%)\n"
                )
                f.write(
                    f"Prosjecan broj poteza: {result['avg_moves']:.1f}\n"
                )
                f.write(
                    f"Prosjecno vrijeme Heuristic: "
                    f"{result['avg_heuristic_time'] * 1000:.2f} ms\n"
                )
                f.write(
                    f"Prosjecno vrijeme Neural:    "
                    f"{result['avg_neural_time'] * 1000:.2f} ms\n"
                )
                f.write("\n")

            f.write("=== Pregled rezultata ===\n")
            f.write(
                f"{'Depth':<8}"
                f"{'Heur. wins':<14}"
                f"{'Neural wins':<14}"
                f"{'Draws':<10}"
                f"{'Avg moves':<12}"
                f"{'Heur. ms':<12}"
                f"{'Neural ms':<12}\n"
            )
            f.write("-" * 82 + "\n")

            for result in results:
                f.write(
                    f"{result['depth']:<8}"
                    f"{result['heuristic_wins']:<14}"
                    f"{result['neural_wins']:<14}"
                    f"{result['draws']:<10}"
                    f"{result['avg_moves']:<12.1f}"
                    f"{result['avg_heuristic_time'] * 1000:<12.2f}"
                    f"{result['avg_neural_time'] * 1000:<12.2f}\n"
                )
            f.write("\n")

    return results


if __name__ == "__main__":
    run_all_depths(save_path="data/depth_test_results.txt")