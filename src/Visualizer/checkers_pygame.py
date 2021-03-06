# Import packages
from src.RulesModule import rules
from src.VisionModule import image_processing
from src.RulesModule.board import Board
from src.VisionModule.image_processing import load_configs_dict

import pygame
import math
import time

# Inititalize Pieces
empty = 0
# For the first move, black's pieces are considered friendly
black = {"pawn": 1, "king": 3}
white = {"pawn": 2, "king": 4}

# Initalize board size
rows = 8
columns = 8


# Define colours
class Colours:
    d = load_configs_dict("../configs/color_config.txt")
    square_black = (0, 0, 0)
    square_white = (255, 255, 255)

    piece_white = tuple(reversed(d["COLOR_TOP"]))
    piece_black = tuple(reversed(d["COLOR_BOT"]))
    king_cross = (255, 255, 255)


# This sets the width, height and margin of each board cell
window_size = [1000, 1000]
window_width = window_size[0]
window_height = window_size[1] - window_size[0] // 20
total_rows = 8
total_columns = 8
width = (window_width // total_columns)
height = (window_height // total_rows)

# Set the radius and border border of each checker piece
radius = (window_width // 20)
border = (window_width // 200)


# Create board
def create_board():
    board = [[empty for column in range(columns)] for row in range(rows)]
    place_starting_pieces(board)
    return board


def place_starting_pieces(board):
    """Assign starting checker pieces for white and black"""
    # Assign starting board locations for black
    for current_row in range(5, 8, 2):
        for current_column in range(0, 8, 2):
            board[current_row][current_column] = black['pawn']
    for current_row in range(6, 7):
        for current_column in range(1, 8, 2):
            board[current_row][current_column] = black['pawn']

    # Assign starting board locations for white
    for current_row in range(0, 3, 2):
        for current_column in range(1, 8, 2):
            board[current_row][current_column] = white['pawn']
    for current_row in range(1, 2):
        for current_column in range(0, 8, 2):
            board[current_row][current_column] = white['pawn']


def draw_board(screen, board, width, height, radius, border):
    for row in range(8):
        for column in range(8):
            # Draw all grid locations as either white or black rectangle
            if (row + column) % 2 == 0:
                colour = Colours.square_white
            else:
                colour = Colours.square_black
            rect = pygame.draw.rect(screen, colour, [width * column, height * row, width, height])
            rect_center = rect.center
            # Draw black pieces
            if board[row][column] == 1:
                pygame.draw.circle(screen, Colours.piece_black, rect_center, radius)
            # Draw white pieces
            if board[row][column] == 2:
                pygame.draw.circle(screen, Colours.piece_white, rect_center, radius)
            # Drawing king pieces borders
            if board[row][column] == 3:
                pygame.draw.circle(screen, Colours.piece_black, rect_center, radius)
                pygame.draw.circle(screen, Colours.king_cross, rect_center, radius // 5, 0)
            if board[row][column] == 4:
                pygame.draw.circle(screen, Colours.piece_white, rect_center, radius)
                pygame.draw.circle(screen, Colours.king_cross, rect_center, radius // 5, 0)


def draw_popup(screen, message, colour, error):
    rect = pygame.Rect(0, window_height, window_width, window_height // 5)
    pygame.draw.rect(screen, colour, rect, 0)

    font_size = 30
    if error is True:
        font_size /= 1.5

    myfont = pygame.font.SysFont('Arial', int(font_size))
    textsurface = myfont.render(message, False, (0, 0, 0))
    if error is True:
        screen.blit(textsurface, (0, window_height))
    else:
        screen.blit(textsurface, (window_width // 2 - 120, window_height))


def get_cell_coordinates(cell_no):
    cell_no = int(cell_no)

    y = (cell_no // 4)
    x = 2 * ((cell_no - 1) % 4)

    if cell_no % 4 == 0:
        y = y - 1

    if y % 2 == 0:
        x = x + 1

    return [y, x]


def get_cell_no(x, y):
    if x % 2 == 0 and y % 2 == 1:
        return math.ceil(x / 2) + (y * 4) + 1

    elif x % 2 == 1 and y % 2 == 0:
        return math.ceil(x / 2) + (y * 4)

    # White cell
    else:
        return 0


def move_piece(screen, board, cell_from, cell_to, became_queen):
    xyfrom = get_cell_coordinates(cell_from)
    xyto = get_cell_coordinates(cell_to)

    piece = board[xyfrom[0]][xyfrom[1]]
    if became_queen is not None and piece <= 2:
        piece += 2

    board[xyfrom[0]][xyfrom[1]] = empty
    board[xyto[0]][xyto[1]] = piece

    draw_board(screen, board, width, height, radius, border)
    pygame.display.flip()
    time.sleep(1)


def remove_piece(screen, board, cell):
    if cell == 0:
        return
    else:
        xycaptured = get_cell_coordinates(cell)
        board[xycaptured[0]][xycaptured[1]] = empty

    draw_board(screen, board, width, height, radius, border)
    pygame.display.flip()
    time.sleep(1)


import os


def run_visualizer():
    abs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "pictures/newtest2"))

    previous_board = Board(os.path.join(abs_dir, "000.png"))
    next_board = Board(os.path.join(abs_dir, "001.png"))
    previous_board.validate_initially(True)
    move = rules.try_to_get_move_category(previous_board, next_board)

    game_over = False
    board = create_board()

    # Initalize pygame
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()

    draw_board(screen, board, width, height, radius, border)
    pygame.display.flip()
    time.sleep(2)

    for ix, img_path in enumerate(sorted(os.listdir(abs_dir))):
        img_path = os.path.join(abs_dir, img_path)
        print(ix, img_path)
        if ix == 0:
            continue
        if ix == 1:
            continue

        if move is not None:
            if move["captured"] == 0:
                move_notation = move["move"].split("-")
            else:
                move_notation = move["move"].split("x")

            old_cell = move_notation[0]
            new_cell = move_notation[1]

            draw_popup(screen, "Valid move: " + move["move"], (50, 150, 255), error=False)

            # Moving the pieces
            move_piece(screen, board, old_cell, new_cell, move["becameQueen"])
            remove_piece(screen, board, move["captured"])

        try:
            previous_board = next_board
            next_board = Board(img_path)
            move = rules.try_to_get_move_category(previous_board, next_board)
            print(move)
        except Exception as exception:
            print(str(exception))
            draw_popup(screen, str(exception), (255, 55, 50), error=True)
            pygame.display.flip()
            time.sleep(5)

    clock.tick(144)



run_visualizer()
