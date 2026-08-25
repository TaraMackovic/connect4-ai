from .board import ROWS, COLS

def check_win(board, player):

    #horizontalno
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    #vertikalno
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    #dijagonalno (glavna \)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    #dijagonalno (sporedna /)
    for row in range(3, ROWS):
        for col in range(COLS - 3):   
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(board[0][col] != 0 for col in range(COLS))
   
def get_game_result(board):
    if check_win(board, 1):
        return 1
    if check_win(board, 2):
        return 2
    if is_board_full(board):
        return "draw"

    return None


if __name__ == "__main__":

    horizontal_win = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
    ]

    print("Result: ", get_game_result(horizontal_win)) #1
 
    vertical_win = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
    ]

    print("Result: ", get_game_result(vertical_win)) #2

    diagonal_win_main = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0, 0, 0],
            [0, 1, 1, 2, 0, 0, 0],
            [0, 1, 2, 1, 2, 0, 0],
        ]
    
    print("Result: ", get_game_result(diagonal_win_main)) #2
 
    diagonal_win = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 2, 0, 0, 0],
        [0, 1, 2, 2, 0, 0, 0],
        [1, 2, 2, 1, 0, 0, 0],
    ]

    print("Result: ", get_game_result(diagonal_win)) #1

    board_full = [
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1],
    ]
    
    print("Result: ", get_game_result(board_full)) #draw
 
    no_win = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 1, 0, 0, 0],
    ]

    print("Result: ", get_game_result(no_win)) #None
 