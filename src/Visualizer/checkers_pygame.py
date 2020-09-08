# Import packages
from src.RulesModule import rules
from src.VisionModule import image_processing
from src.RulesModule.board import Board

import pygame
import math
import time

# Communication interface - post moves here in that list
class MoveQueue:
    queue = []


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
    square_black = (0, 0, 0)
    square_white = (255, 255, 255)

    piece_white = (247, 255, 191)
    piece_black = (51, 8, 0)
    piece_black_border = (91, 38, 30)
    king_gold = (255, 215, 0)


# Create board
def create_board():
    board = [[empty for column in range(columns)] for row in range(rows)]
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
                # Draw border around black pieces
                pygame.draw.circle(screen, Colours.piece_black_border, rect_center, radius, border)
            # Draw white pieces
            if board[row][column] == 2:
                pygame.draw.circle(screen, Colours.piece_white, rect_center, radius)
            # Drawing king pieces borders
            if board[row][column] == 3:
                pygame.draw.circle(screen, Colours.piece_black, rect_center, radius)
                pygame.draw.circle(screen, Colours.king_gold, rect_center, radius, border)
            if board[row][column] == 4:
                pygame.draw.circle(screen, Colours.piece_white, rect_center, radius)
                pygame.draw.circle(screen, Colours.king_gold, rect_center, radius, border)


def get_cell_coordinates(cell_no):
    cell_no = int(cell_no)

    y = (cell_no // 4)
    x = 2 * ((cell_no - 1) % 4)

    if cell_no % 4 == 0:
        y = y - 1

    if y % 2 == 0:
        x = x + 1

    return [x, y]


def get_cell_no(x, y):
    if x % 2 == 0 and y % 2 == 1:
        return math.ceil(x / 2) + (y * 4) + 1

    elif x % 2 == 1 and y % 2 == 0:
        return math.ceil(x / 2) + (y * 4)

    # White cell
    else:
        return 0


def start_visualizer():
    name = "plansza0x.png"
    previous_board = Board(name.replace("x", str(0)))
    next_board = Board(name.replace("x", str(1)))
    MoveQueue.queue.append(rules.try_to_get_move_category(previous_board, next_board))
    i = 2

    # Initalize vairables
    game_over = False
    board = create_board()
    place_starting_pieces(board)

    # Initalize pygame
    pygame.init()
    window_size = [1000, 1000]
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Checkers")
    # icon = pygame.image.load("logo.png")
    # pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # This sets the width, height and margin of each board cell
    window_width = window_size[0]
    window_height = window_size[1]
    total_rows = 8
    total_columns = 8
    width = (window_width // total_columns)
    height = (window_height // total_rows)

    # Set the radius and border border of each checker piece
    radius = (window_width // 20)
    border = (window_width // 200)

    # Main active game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Try to read move queue
            else:
                if len(MoveQueue.queue) > 0:
                    # Processing the move
                    move = MoveQueue.queue[0]
                    print(move)

                    if move["captured"] == 0:
                        move_notation = move["move"].split("-")

                    else:
                        move_notation = move["move"].split("x")

                    old_cell = move_notation[0]
                    new_cell = move_notation[1]
                    old_coords = get_cell_coordinates(old_cell)
                    new_coords = get_cell_coordinates(new_cell)

                    # Moving the pieces
                    board[old_coords[0]][old_coords[1]] = empty

                    if move["player"] == "WHITE":
                        board[new_coords[0]][new_coords[1]] = white["pawn"]
                    elif move["player"] == "BLACKED":
                        board[new_coords[0]][new_coords[1]] = black["pawn"]

                    if move["captured"] != 0:
                        captured_cell = move["captured"]
                        captured_coords = get_cell_coordinates(captured_cell)
                        board[captured_coords[0]][captured_coords[1]] = empty

                    MoveQueue.queue.pop(0)
                    time.sleep(1)
                try:
                    previous_board = next_board
                    next_board = Board(name.replace("x", str(i)))
                    MoveQueue.queue.append(rules.try_to_get_move_category(previous_board, next_board))
                except Exception as exception:
                    print("exception")
                i = i + 1

        clock.tick(144)
        draw_board(screen, board, width, height, radius, border)
        pygame.display.flip()

    pygame.quit()


start_visualizer()

