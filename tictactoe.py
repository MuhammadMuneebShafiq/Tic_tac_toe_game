"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    lines = []
    for i in range(3):
        lines.append(board[i])
    for j in range(3):
        lines.append([board[i][j] for i in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])
    for line in lines:
        if line.count(X) == 3:
            return X
        if line.count(O) == 3:
            return O
    return None


def terminal(board):
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        v = -math.inf
        best_move = None
        for action in actions(board):
            val = min_value(result(board, action))
            if val > v:
                v = val
                best_move = action
        return best_move
    else:
        v = math.inf
        best_move = None
        for action in actions(board):
            val = max_value(result(board, action))
            if val < v:
                v = val
                best_move = action
        return best_move


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
