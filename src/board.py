import cv2.cv2 as cv2


class Board:
    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]

    def get_board(self):
        return self.board
