from unittest import TestCase
from src.board import Board

class TestBoard(TestCase):
    def test_get_board(self):
        t = Board()
        b = t.get_board()
        for i in b:
            print(i)