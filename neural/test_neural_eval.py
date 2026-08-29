from search.minmax import State, maximize_ab
from neural.neural_eval import evaluate as evaluate_neural


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
    score, next_state = maximize_ab(state, depth=3,eval_function=evaluate_neural)
    print(f"AI odigrao kolonu {next_state.last_move} (ocjena: {score:.4f})")


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
    score, next_state = maximize_ab(state, depth=3,eval_function=evaluate_neural)
    print(f"AI odigrao kolonu {next_state.last_move} (ocjena: {score:.4f})")

def test3():
    state = State(curr_player=1)
    score, next_state = maximize_ab(state, depth=3,eval_function=evaluate_neural)
    print(f"AI odigrao kolonu {next_state.last_move} (ocjena: {score:.4f})")
    
if __name__ == "__main__":
    test1()
    test2()
    test3()
