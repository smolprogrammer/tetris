import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARIABLES
s_width = 800
s_height = 700
play_width = 300  # 300 // 10 = 30 width per block
play_height = 600  # 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape
# 0 = S
# 1 = Z
# 2 = I
# 3 = O
# 4 = J
# 5 = L
# 6 = T


class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, row, column, shape):
        self.x = row
        self.y = column
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for column in range(10)] for row in range(20)]

    # if there already are placed figures then blank grid will change
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if (column, row) in locked_positions:
                figure = locked_positions[(column, row)]
                grid[row][column] = figure
    return grid


def convert_shape_format(shape):
    positions = []
    formatted = shape.shape[shape.rotation % len(shape.shape)]

    for index, row in enumerate(formatted):
        rows = list(row)
        for indx, column in enumerate(rows):
            if column == '0':
                positions.append((shape.x + indx, shape.y + index))

    for index, pos in enumerate(positions):
        positions[index] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(column, row) for column in range(10) if grid[row][column] == (0, 0, 0)] for row in range(20)]
    accepted_pos = [column for sub in accepted_pos for column in sub]
    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('Calibri', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, rows, cols):
    sx = top_left_x  # start x
    sy = top_left_y  # start y

    for row in range(rows):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + row * block_size),
                         (sx + play_width, sy + row * block_size))
        for column in range(cols):
            pygame.draw.line(surface, (128, 128, 128), (sx + column * block_size, sy),
                             (sx + column * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    for rows in range(len(grid)-1, -1, -1):
        row = grid[rows]
        if (0, 0, 0) not in row:
            inc += 1
            ind = rows
            for column in range(len(row)):
                try:
                    del locked[(column, rows)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Calibri', 30)
    label = font.render('Next Shape is:', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    formatted = shape.shape[shape.rotation % len(shape.shape)]

    for index, row in enumerate(formatted):
        rows = list(row)
        for indx, column in enumerate(rows):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + indx * block_size, sy + index * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def draw_window(surface, score=0):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont("Calibri", 60)
    label = font.render("TETRIS", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('Calibri', 30)
    label = font.render(f'Score: {str(score)}', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 30, sy + 160))

    font = pygame.font.SysFont('Calibri', 30)
    label = font.render(f'Highest score so far: {max_score()}', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 425

    surface.blit(label, (sx - 100, sy + 70))

    for row in range(len(grid)):
        for column in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][column], (top_left_x + column * block_size, top_left_y + row * block_size, block_size, block_size), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    score = 0

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece += 1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            if clear_rows(grid, locked_positions):
                score += clear_rows(grid, locked_positions) * 10
            #  score += clear_rows(grid, locked_positions) * 10

            clear_rows(grid, locked_positions)

        draw_window(win, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost:(", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)
    update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to play!', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRIS')
main_menu(win)  # start game
