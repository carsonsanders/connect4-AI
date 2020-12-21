

"""
returns list of tuples showing the possible positions
"""
from copy import deepcopy


def action(state):
    actions = []
    if terminal(state):
        return actions  # return an empty list of actions, game is over
    for col in range(len(state[0])):
        row = len(state) - 1  # bottom of the column
        while row >= 0 and state[row][col] != '':
            row -= 1
        if row >= 0:
            actions.append((row, col))
    return actions


def result(state, move, player):
    new_state = deepcopy(state)
    new_state[move[0]][move[1]] = player
    return new_state


def terminal(state):
    if win(state) or draw(state):
        return True
    else:
        return False


# tells if the given state has a winning player, and which player it is
def win(state):
    for row in range(len(state)):
        for col in range(len(state[0])):
            if row + 3 < len(state):  # check connecting dots vertically
                if state[row][col] != '' \
                        and state[row][col] == state[row+1][col] == state[row+2][col] == state[row+3][col]:
                    return state[row][col]
            if col + 3 < len(state[0]):  # check connecting dots horizontally
                if state[row][col] != '' \
                        and state[row][col] == state[row][col+1] == state[row][col+2] == state[row][col+3]:
                    return state[row][col]
            if row + 3 < len(state) and col+3 < len(state[0]):  # check connecting dots diagonally downwards
                if state[row][col] != '' \
                        and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return state[row][col]
            if row + 3 < len(state) and col-3 >= 0:  # check connecting dots diagonally upwards
                if state[row][col] != '' \
                        and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return state[row][col]
    return ''  # no winner yet


# tells if the given state is a draw game
def draw(state):
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] == '':
                return False
    return True


# evaluates the state of the board for the given player
def evaluation_function(state, player):
    if terminal(state):
        if win(state) == player:
            return float('inf')      # maximum possible score if the player wins
        elif draw(state):
            return 0  # draw state gives 0
        else:
            return -float('inf')  # minimum possible if the other player wins
    else:  # game is going we need to evaluate player points
        return heuristic(state, player)


def heuristic(state, player):
    game_state_score = 0
    visited = set()
    for limit in range(2, 0, -1):  # discover patterns in limit of 2, 1, 0
        for row in range(len(state)):
            for col in range(len(state[0])):
                if (row, col) not in visited:
                    lists = []
                    list_1_val = []
                    list_1_cord = []
                    lists.append((list_1_val, list_1_cord))

                    list_2_val = []
                    list_2_cord = []
                    lists.append((list_2_val, list_2_cord))

                    list_3_val = []
                    list_3_cord = []
                    lists.append((list_3_val, list_3_cord))

                    list_4_val = []
                    list_4_cord = []
                    lists.append((list_4_val, list_4_cord))

                    for move in range(limit+1):  # inclusive limit
                        # move to bottom from center

                        if row+move < len(state) and (row+move, col) not in visited and state[row][col] != '' and (
                                len(list_1_val) == 0 or state[row+move][col] in list_1_val):
                            list_1_val.append(state[row+move][col])
                            list_1_cord.append((row+move, col))

                        # move to top from center

                        if 0 <= row - move and (row - move, col) not in visited and state[row][col] != '' and (
                                len(list_2_val) == 0 or state[row - move][col] in list_2_val):
                            list_2_val.append(state[row-move][col])
                            list_2_cord.append((row - move, col))

                        # move to left from center

                        if 0 <= col - move and (row, col-move) not in visited and state[row][col] != '' and (
                                len(list_3_val) == 0 or state[row][col-move] in list_3_val):
                            list_3_val.append(state[row][col-move])
                            list_3_cord.append((row, col-move))

                        # move to left from center

                        if col + move < len(state[0]) and (row, col+move) not in visited and state[row][col] != '' and (
                                len(list_4_val) == 0 or state[row][col+move] in list_4_val):
                            list_4_val.append(state[row][col+move])
                            list_4_cord.append((row, col+move))

                    # evaluate all lists
                    for (list_val, list_cord) in lists:
                        if len(list_val) == limit+1:
                            game_state_score += score(list_val, limit+1, player)
                            for coordinates in list_cord:
                                visited.add(coordinates)

    # print(game_state_score)
    return game_state_score


def score(list_val, size, player):
    score = 0
    if size == 3:
        if list_val[0] == player:
            score += 50
        else:
            score -= 50
    elif size == 2:
        if list_val[0] == player:
            score += 25
        else:
            score -= 25
    elif size == 1:
        if list_val[0] == player:
            score += 10
        else:
            score -= 10
    return score
