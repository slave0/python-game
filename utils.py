from random import randint as rand
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def rand_bool (r, mxr):
    t = rand(0, mxr)
    return (t <= r)

def rand_cell (width, height):
    return (rand(0, width - 1), rand(0, height - 1))

def rand_rive_cell(x, y, moves):
    t = rand(0, len(moves) - 1)
    dx, dy = moves[t][0], moves[t][1]
    return (x + dx, y + dy)

def get_moves(x, y, cells):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    result = []

    for move in moves:
        moveX, moveY = move[0], move[1]
        cellX, cellY = x + moveX, y + moveY

        if (not check_bounds(cellX, cellY, len(cells[0]), len(cells))):
             continue

        if (cells[cellY][cellX] == 2):
            continue

        result.append(move)

    return result

def check_bounds(x, y, width, height):
    if (x < 0 or y < 0 or x >= width or y >= height):
            return False
    return True