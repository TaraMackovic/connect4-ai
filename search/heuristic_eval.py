from game.board import ROWS, COLS, print_board

CENTER_BONUS = 3
THREE_IN_WINDOW = 5
TWO_IN_WINDOW = 2
WIN_SCORE = 1000  


def evaluate_window(window, player, opponent):
    score = 0
    player_count = window.count(player)
    opp_count = window.count(opponent)
    empty_count = window.count(0)

    if player_count == 4:
        score += WIN_SCORE
    elif player_count == 3 and empty_count == 1:
        score += THREE_IN_WINDOW
    elif player_count == 2 and empty_count == 2:
        score += TWO_IN_WINDOW

    if opp_count == 4:
        score -= WIN_SCORE
    elif opp_count == 3 and empty_count == 1:
        score -= THREE_IN_WINDOW
    elif opp_count == 2 and empty_count == 2:
        score -= TWO_IN_WINDOW

    return score


def evaluate(board, player):
    opponent = 2 if player == 1 else 1
    score = 0

    # centralna kolona 
    center_col_index = COLS // 2
    center_column = [board[r][center_col_index] for r in range(ROWS)]
    score += center_column.count(player) * CENTER_BONUS
    score -= center_column.count(opponent) * CENTER_BONUS

    # horizontalni prozori
    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            window = row[c:c + 4]
            score += evaluate_window(window, player, opponent)

    # vertikalni prozori
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col[r:r + 4]
            score += evaluate_window(window, player, opponent)

    # dijagonala (glavna \)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # dijagonala (sporedna /)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    return score


if __name__ == "__main__":

    board1 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
    ]
    print_board(board1)
    print("Igrac 1: ", evaluate(board1, 1))
    print("Igrac 2: ", evaluate(board1, 2), "\n")

    board2 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [2, 1, 1, 2, 2, 0, 0],  
    ]
    print_board(board2)
    print("Igrac 1: ", evaluate(board2, 1))
    print("Igrac 2: ", evaluate(board2, 2))
    