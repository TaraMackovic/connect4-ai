from search.minmax import State, maximize_ab
from search.heuristic_eval import evaluate as evaluate_heuristic


def test1():
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
    ]
    state = State(board, curr_player=1)
    score, next_state = maximize_ab(state, depth=4,eval_function=evaluate_heuristic)
    print(f"AI odigrao kolonu {next_state.last_move}")


def test2():
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 2, 0, 0, 0],
    ]

    state = State(board, curr_player=1)
    score, next_state = maximize_ab(state, depth=4,eval_function=evaluate_heuristic)
    print(f"AI odigrao kolonu {next_state.last_move}")


def test3():
    state = State(curr_player=1)
    score, next_state = maximize_ab(state, depth=2,eval_function=evaluate_heuristic)
    print(f"AI bira kolonu {next_state.last_move}")

if __name__ == "__main__":
    test1()
    test2()
    test3()
