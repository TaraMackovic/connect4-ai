# Minimalna verzija
# TODO: Prosiriti

from game.board import print_board
from game.rules import get_game_result
from search.minmax import State, maximize_ab, minimize_ab, clear_transposition_table
from search.heuristic_eval import evaluate as evaluate_heuristic
from neural.neural_eval import evaluate as evaluate_neural

HEURISTIC_PLAYER = 1
NEURAL_PLAYER = 2
DEPTH = 3

def play_one_game():

    clear_transposition_table()
    state = State(curr_player=HEURISTIC_PLAYER)

    while True:
        print_board(state.board)
        result = get_game_result(state.board)
        if result is not None:
            print("Rezultat:", result)
            break

        if state.curr_player == HEURISTIC_PLAYER:
            print("Heuristic agent na redu...")
            _, next_state = maximize_ab(state, depth=DEPTH, eval_function=evaluate_heuristic)
        else:
            print("Neural agent na redu...")
            _, next_state = minimize_ab(state, depth=DEPTH, eval_function=evaluate_neural)

        if next_state is None:
            print("Greska: minmax nije vratio sledece stanje!")
            break

        state = next_state
        print(f"Odigrana kolona: {state.last_move + 1}\n")

if __name__ == "__main__":
    play_one_game()