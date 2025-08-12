0def print_board(board):
    print("-" * 10)
    for row in board:
        print(" | ".join(row))
        print("-" * 10)
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None
def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score
def ai_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = "O"
def player_move(board):
    while True:
        try:
            row = int(input("Enter row (0 to 2): "))
            col = int(input("Enter column (0 to 2): "))
            if board[row][col] == " ":
                board[row][col] = "X"
                break
            else:
                print("That place is taken. Try again.")
        except:
            print("Invalid input. Enter numbers between 0 and 2.")
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe")
    print("You are X | AI is O")
    print_board(board)

    while True:
        player_move(board)
        print_board(board)
        if check_winner(board):
            print("You win!" if check_winner(board) == "X" else "AI wins!")
            break
        if is_draw(board):
            print("Match Drawn!")
            break

        ai_move(board)
        print("AI has played:")
        print_board(board)
        if check_winner(board):
            print("You win!" if check_winner(board) == "X" else "AI wins!")
            break
        if is_draw(board):
            print("Match Drawn!")
            break
if __name__ == "__main__":
    play_game()
