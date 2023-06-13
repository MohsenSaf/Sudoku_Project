import numpy as np
import time

start_time = time.perf_counter()


file_name = "medium"


def set_input(fname):
    with open(fname, "r") as f:
        rows = f.read().strip().split("\n")

        matrix = [list(map(int, row.split())) for row in rows]

        np_array = np.array(matrix)
        return np_array


input = set_input(f"{file_name}.txt")


def goal_test(state):
    return not 0 in state


def heuristic(state):
    return np.count_nonzero(state == 0)


table = [heuristic(input), input]


def row(state, i):
    return state[i, :]


def column(state, j):
    return state[:, j]


def box(state, n):
    fc = (n % 3) * 3
    lc = fc + 3

    fr = (n // 3) * 3
    lr = fr + 3

    return state[fr:lr, fc:lc]


fringe = []

fringe.append([heuristic(input), input])


def best_empty_pos(state):
    l = []
    for i in range(9):
        for j in range(9):
            if state[i, j] == 0:
                non_zero = 0
                non_zero += np.count_nonzero(row(state, i))
                non_zero += np.count_nonzero(column(state, j))
                non_zero += np.count_nonzero(box(state, ((i // 3) * 3 + j // 3)))
                l.append((non_zero, (i, j)))
    if not l:
        return None
    return max(l)[1]


def rule(state, palce, num):
    i, j = palce
    k = (i // 3) * 3 + j // 3
    if num in row(state, i):
        return False
    if num in column(state, j):
        return False
    if num in box(state, k):
        return False
    return True


def create_output(state):
    output = ""
    output += "╔" + ((9 * "═") + "╦") * 2 + (9 * "═") + "╗" + "\n"
    for i in range(9):
        if i % 3 == 0 and i != 0:
            output += "╠" + ((9 * "═") + "╬") * 2 + (9 * "═") + "╣" + "\n"
        row = ""
        for j in range(9):
            if j % 3 == 0:
                row += "║"
            row += " {} ".format(state[i, j])
            if j == 8:
                row += "║"
        output += row + "\n"
    output += "╚" + ((9 * "═") + "╩") * 2 + (9 * "═") + "╝" + "\n"

    with open(f"{file_name}_solution.txt", "w", encoding="utf-8") as f:
        f.write(f"{output}\n")


def Astar(fringe):
    while True:
        fringe.sort(reverse=True, key=lambda x: x[0])
        best_state = fringe.pop()
        f = best_state[0] - heuristic(best_state[1]) + 1
        best_state = best_state[1]
        if goal_test(best_state):
            create_output(best_state)
            print(best_state)
            break
        next_empty = best_empty_pos(best_state)
        for i in range(1, 10):
            if rule(best_state, next_empty, i):
                new_state = best_state.copy()
                new_state[next_empty] = i
                fringe.append([f + heuristic(new_state), new_state])


Astar(fringe)

print("---- %s seconds ----" % (time.perf_counter() - start_time))
