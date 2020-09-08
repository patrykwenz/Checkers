from src.Visualizer import checkers_pygame
from src.RulesModule import rules
from src.VisionModule import image_processing
from src.RulesModule.board import Board

if __name__ == '__main__':
    name = "plansza0x.png"
    previous_board = Board(name.replace("x", str(0)))
    next_board = Board(name.replace("x", str(1)))
    queue = [rules.try_to_get_move_category(previous_board, next_board)]
    i = 2
    checkers_pygame.start_visualizer()

    while True:
        if len(queue) > 0:
            checkers_pygame.MoveQueue.queue.append(queue[0])
            queue.pop(0)
        try:
            previous_board = next_board
            next_board = Board(name.replace("x", str(i)))
            queue.append(rules.try_to_get_move_category(previous_board, next_board))
        except Exception as ex:
            print("Exception thrown")
        i = i + 1
