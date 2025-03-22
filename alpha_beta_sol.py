import math


X = "X"
O = "O"
EMPTY = None

def initial_state():
    """Returns the starting Tic Tac Toe board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """Returns the player whose turn it is (X or O)."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    """Returns the set of possible moves (i, j) on the board."""
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    """Returns the board after making a move."""
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action")
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """Returns the winner (X, O, or None)."""
    lines = (board +                          
             [[board[i][j] for i in range(3)] for j in range(3)] +  #
             [[board[i][i] for i in range(3)],                     
              [board[i][2 - i] for i in range(3)]])                
    for line in lines:
        if line.count(X) == 3:
            return X
        if line.count(O) == 3:
            return O
    return None

def terminal(board):
    """Checks if the game is over."""
    return winner(board) is not None or all(EMPTY not in row for row in board)

def utility(board):
    """Returns the utility value: 1 if X wins, -1 if O wins, 0 if draw."""
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def max_value(board, alpha, beta):
    """Maximizer's evaluation with alpha-beta pruning, returns (value, nodes_visited)."""
    if terminal(board):
        return utility(board), 1  
    v = -math.inf
    nodes_visited = 0
    for action in actions(board):
        val, nodes = min_value(result(board, action), alpha, beta)
        v = max(v, val)
        nodes_visited += nodes
        if v >= beta:
            return v, nodes_visited + 1  
        alpha = max(alpha, v)
    return v, nodes_visited + 1  

def min_value(board, alpha, beta):
    """Minimizer's evaluation with alpha-beta pruning, returns (value, nodes_visited)."""
    if terminal(board):
        return utility(board), 1  
    v = math.inf
    nodes_visited = 0
    for action in actions(board):
        val, nodes = max_value(result(board, action), alpha, beta)
        v = min(v, val)
        nodes_visited += nodes
        if v <= alpha:
            return v, nodes_visited + 1  
        beta = min(beta, v)
    return v, nodes_visited + 1  

def minimax(board):
    """Returns the optimal move and total nodes visited."""
    if player(board) == X: 
        v = -math.inf
        best_move = None
        total_nodes = 1  
        for action in actions(board):
            val, nodes = min_value(result(board, action), -math.inf, math.inf)
            total_nodes += nodes
            if val > v:
                v = val
                best_move = action
        return best_move, total_nodes
    else:  
        v = math.inf
        best_move = None
        total_nodes = 1  
        for action in actions(board):
            val, nodes = max_value(result(board, action), -math.inf, math.inf)
            total_nodes += nodes
            if val < v:
                v = val
                best_move = action
        return best_move, total_nodes

def print_board(board):
    """Displays the board."""
    for i in range(3):
        print("|".join([board[i][j] if board[i][j] != EMPTY else " " for j in range(3)]))
        if i < 2:
            print("-+-+-")

def main():
    """Runs the Tic Tac Toe game and prints nodes visited by the computer."""
    board = initial_state()
    print("Welcome to Tic Tac Toe! You are X, computer is O.")
    print("Enter moves as row and column numbers from 1 to 3.")
    print_board(board)
    while not terminal(board):
        if player(board) == X:
            print("Your turn (X).")
            try:
                row = int(input("Row: ")) - 1
                col = int(input("Column: ")) - 1
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == EMPTY:
                    board = result(board, (row, col))
                else:
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Enter numbers 1 to 3.")
                continue
        else:
            print("Computer's turn (O).")
            move, nodes_visited = minimax(board)
            print(f"Computer visited {nodes_visited} nodes.")
            board = result(board, move)
        print_board(board)
    win = winner(board)
    print("You win!" if win == X else "Computer wins!" if win == O else "It's a draw!")

if __name__ == "__main__":
    main()