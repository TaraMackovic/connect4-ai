ROWS = 6
COLS = 7

""" igrac1 = 1, igrac2 = 2, empty = 0
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


def print_board(board):
    for i in range(ROWS):
        print(" ".join(map(str, board[i])))

if __name__ == "__main__":
    board = create_board()
    print_board(board)