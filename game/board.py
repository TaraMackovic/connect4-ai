ROWS = 6
COLS = 7

""" player1 = 1, player2 = 2, empty = 0
board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0],
    [0, 1, 2, 2, 2, 1, 0],
]
"""

def create_board():
    return [[0 for i in range(COLS)] for j in range(ROWS)]

def copy_board(board):
    return [list(row) for row in board]

def print_board(board):
    for i in range(ROWS):
        print(" ".join(map(str, board[i])))


def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False 

    return board[0][col] == 0

def get_legal_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def get_next_empty_row(board, col):
    for i in range(ROWS -1, -1, -1):
        if board[i][col] == 0:
            return i

    return None

def make_move(board, col, player):
    if not is_valid_move(board, col):
        return False

    row = get_next_empty_row(board, col)
    board[row][col] = player
    return row, col

def undo_move(board, row, col):
    board[row][col] = 0


def play_game():
    from rules import get_game_result

    board = create_board()
    player = 1

    while True:
        print_board(board)

        print(f"Igrac {player}, izaberi kolonu (1-{COLS}): ")
        col = int(input()) - 1

        if not make_move(board, col, player):
            print(f"Nevalidan potez: Igrac {player} igra ponovo.")
            continue

        result = get_game_result(board)

        if result == "draw":
            print_board(board)
            print("Izjednaceno!")
            break
        elif result is not None:
            print_board(board)
            print("Pobijednik je igrac: ", result)
            break

        if player == 1: player = 2
        else: player = 1

if __name__ == "__main__":
    play_game()