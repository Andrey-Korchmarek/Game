import numpy as np
from itertools import permutations, product
from ursina import *

board_a = range(-4 * 42, 4 * 42, 4)
board_b = range(2 - 4 * 42, 4 * 42 - 2, 4)
a = [(i, j, k) for i in board_a for j in board_a for k in board_a]
b = [(i, j, k) for i in board_b for j in board_b for k in board_b]
cube = [np.array(point) for point in a + b]

faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
faces = [np.array(x) for x in faces]

def generate_board(size):
    global cube
    global faces
    mask = [x * size for x in faces]
    result = [tuple(point) for point in cube if
              all([np.dot(height, point) + np.linalg.norm(height) ** 2 >= 0 for height in mask])]
    return result

current_size = 1

app = Ursina()
