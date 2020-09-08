# Import packages
import pygame
import math

# Communication interface - post moves here in that list
class MoveQueue:
    queue = [{"player": "white", "move": ""}]


# Inititalize Pieces
empty = 0
# For the first move, black's pieces are considered friendly
black = {'pawn': 1, 'king': 3}
white = {'pawn': 2, 'king': 4}

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
    y = cell_no // 5
    if y % 2 == 0:
        x = ((cell_no % 5) * 2) - 1
    else:
        x = (cell_no % 5) * 2

    return x, y


def get_cell_no(x, y):
    if x % 2 == 0 and y % 2 == 1:
        return math.ceil(x / 2) + (5 * y)

    elif x % 2 == 1 and y % 2 == 0:
        return math.ceil(x / 2) + (5 * y)

    # White cell
    else:
        return 0

def start_visualizer():
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

            # debug
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_pos = pygame.mouse.get_pos()
                x = (current_pos[0] // width)
                y = (current_pos[1] // height)
                cell = get_cell_no(x, y)
                print(cell)
                print(get_cell_coordinates(cell))

            elif event.type == pygame.QUIT:
                game_over = True

            # Try to read move queue
            else:
                if len(MoveQueue.queue) > 0:
                    print(MoveQueue.queue[0])
                    MoveQueue.queue.pop(0)

        clock.tick(60)
        draw_board(screen, board, width, height, radius, border)
        pygame.display.flip()

    pygame.quit()

