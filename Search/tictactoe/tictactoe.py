"""
Tic Tac Toe Player
"""

import math
import copy

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
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X or board[i][j] == O:
                count += 1
    return X if count % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    for i in range(3):
        for j in range(3):
            if (i, j) == action:
                if board[i][j] == X or board[i][j] == O:
                    raise ValueError("Not possible")
                else:
                    new_board[i][j] = player(board)
                    return new_board
    raise ValueError("Not possible")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2] != EMPTY:
        return board[0][0]
    if board[1][0] == board[1][1] == board[1][2] != EMPTY:
        return board[1][0]
    if board[2][0] == board[2][1] == board[2][2] != EMPTY:
        return board[2][0]
    
    if board[0][0] == board[1][0] == board[2][0] != EMPTY:
        return board[0][0]
    if board[0][1] == board[1][1] == board[2][1] != EMPTY:
        return board[0][1]
    if board[0][2] == board[1][2] == board[2][2] != EMPTY:
        return board[0][2]
    
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    best_move = None
    if player(board) == X:
        # max player
        best = -math.inf
        for action in actions(board):
            new_board = result(board, action)
            res = minimize(new_board)
            if (res > best):
                best = res
                best_move = action
    else:
        # min player
        best = math.inf
        for action in actions(board):
            new_board = result(board, action)
            res = maximize(new_board)
            if (res < best):
                best = res
                best_move = action
    return best_move


def maximize(board):
    if terminal(board):
        return utility(board)
    
    best = -math.inf
    for action in actions(board):
        new_board = result(board, action)
        res = minimize(new_board)
        if (res > best):
            best = res
    return best


def minimize(board):
    if terminal(board):
        return utility(board)
    
    best = math.inf
    for action in actions(board):
        new_board = result(board, action)
        res = maximize(new_board)
        if (res < best):
            best = res
    return best
    