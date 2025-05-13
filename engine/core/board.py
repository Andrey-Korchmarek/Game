import numpy as np
from itertools import permutations, product
from ursina import *

board_a = range(-4 * 42, 4 * 42, 4)
board_b = range(2 - 4 * 42, 4 * 42 - 2, 4)
a = [(i, j, k) for i in board_a for j in board_a for k in board_a]
b = [(i, j, k) for i in board_b for j in board_b for k in board_b]
cube = [np.array(point) for point in a + b]

faces = set(product((1.0, -1.0), repeat=3)).union(*[set(permutations((i, 0.0, 0.0))) for i in (2.0, -2.0)])
faces = [np.array(x) for x in faces]

def generate_board(size):
    global cube
    global faces
    mask = [f * (size + 0.25) for f in faces]
    result = [tuple(int(x) for x in point) for point in cube if
              all([np.dot(height, point) + np.linalg.norm(height) ** 2 > 0.0 for height in mask])]
    return result

current_size = 0
current_board_pos = []
current_board = []

def add_cell(pos):
    color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
    e = Entity(
        model='Cell',
        color=color_calc[sum(pos) % 8],
        position=pos,
    )
    return e

def update_board(new_size):
    global current_board_pos
    global current_board
    previous_board_pos = current_board_pos
    current_board_pos = generate_board(new_size)
    for pos in current_board_pos:
        if pos not in previous_board_pos:
            current_board.append(add_cell(pos))


app = Ursina()
EditorCamera()

border = Entity(
    model='Solid',
    position=(0, 0, 0),
    alpha=0.2,
)


def input(key):
    global current_size
    global border
    if 'a' == key:
        current_size += 1
    if 'w' == key:
        print(current_size)
    if 'd' == key:
        border.scale = current_size + 0.25
        update_board(current_size)

app.run()
