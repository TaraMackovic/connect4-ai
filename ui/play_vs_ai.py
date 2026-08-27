from game.board import print_board, is_valid_move, get_legal_moves
from game.rules import get_game_result
from search.minmax import State, maximize_ab

AI_PLAYER = 1
HUMAN_PLAYER = 2
SEARCH_DEPTH = 5

def get_human_move(board):
    while True:
        try:
            col = int(input(f"Tvoj potez, izaberi kolonu (1-{len(board[0])}): ")) - 1
        except ValueError:
            print("Unesi broj kolone.")
            continue
        if is_valid_move(board, col):
            return col
        print("Nevalidan potez, pokusaj ponovo.")


def play_vs_ai():
    state = State(curr_player=AI_PLAYER)

    while True:
        print_board(state.board)
        result = get_game_result(state.board)

        if result == "draw":
            print("Izjedanceno!")
            break
        elif result == AI_PLAYER:
            print("AI je pobijedio!")
            break
        elif result == HUMAN_PLAYER:
            print("Cestitam, pobijedio si AI-a!")
            break

        if state.curr_player == AI_PLAYER:
            print("AI razmislja...")
            _, next_state = maximize_ab(state, depth=SEARCH_DEPTH)
            state = next_state
            print(f"AI je odigrao kolonu: {state.last_move + 1}")
        else:
            col = get_human_move(state.board)
            state.play_move(col)


if __name__ == "__main__":
    play_vs_ai()