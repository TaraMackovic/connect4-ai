# Heuristic-Agent vs Neural-Agent

import random

from game.board import get_legal_moves
from game.rules import get_game_result
from search.minmax import State, maximize_ab, minimize_ab, clear_transposition_table
from search.heuristic_eval import evaluate as evaluate_heuristic
from neural.neural_eval import evaluate as evaluate_neural

HEURISTIC_PLAYER = 1
NEURAL_PLAYER = 2
DEPTH = 3
NUM_GAMES = 50
RANDOM_OPENING_MOVES = 2

def play_one_game(first_player, rand_opening_moves=RANDOM_OPENING_MOVES):

    clear_transposition_table()
    state = State(curr_player=first_player)
    move_count = 0

    while True:
        result = get_game_result(state.board)
        if result is not None:
            return result, move_count

        # Prvi potezi nausmicni (razbijanje determinizma)
        if move_count < rand_opening_moves:
            col = random.choice(get_legal_moves(state.board))
            state.play_move(col)
            move_count += 1
            continue

        if state.curr_player == HEURISTIC_PLAYER:
            _, next_state = maximize_ab(state, depth=DEPTH, eval_function=evaluate_heuristic)
        else:
            _, next_state = minimize_ab(state, depth=DEPTH, eval_function=evaluate_neural)

        if next_state is None:
            print("Greska: minmax nije vratio sledece stanje!")
            break

        state = next_state
        move_count += 1

def run_tests():
    heuristic_wins = 0
    neural_wins = 0
    draws = 0

    for game_number in range(1, NUM_GAMES + 1):
        if game_number % 2 == 1:
            first_player = HEURISTIC_PLAYER
            first_name = "Heuristic"
        else:
            first_player = NEURAL_PLAYER
            first_name = "Neural"

        result, move_count = play_one_game(first_player)

        if result == HEURISTIC_PLAYER:
            winner = "Heuristic"
            heuristic_wins += 1
        elif result == NEURAL_PLAYER:
            winner = "Neural"
            neural_wins += 1
        else:
            winner = "Draw"
            draws += 1

        print(f"Partija {game_number}: prvi = {first_name}, pobjednik = {winner}, potezi = {move_count}")

    print("\nRezultati:")
    print(f"Heuristic pobjede: {heuristic_wins}")
    print(f"Neural pobjede:    {neural_wins}")
    print(f"Nerijeseno:        {draws}")
    print(f"Ukupno partija:    {NUM_GAMES}")


if __name__ == "__main__":
    run_tests()