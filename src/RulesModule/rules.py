from src.RulesModule.board import Board
from enum import Enum


class MoveCategory(Enum):
    MOVE = 1
    TAKE = 2
    WAS_TAKEN = 3
    MULTIPLE_TAKE = 4
    QUEEN_MOVE = 5
    QUEEN_TAKE = 6
    QUEEN_MULTIPLE_TAKE = 7


def check_if_start(board):
    try:
        board.validate_initially()
    except Exception as e:
        if 'amount' not in str(e):
            raise e
        else:
            return False
    return True


def check_at_start(board):
    board.validate_initially(True)
    board.validate_placement()


def piece_was_moved_from(field_before, field_after):
    if field_before.piece is not None and field_after.piece is None:
        return field_before
    else:
        return field_after


def piece_was_moved_to(field_before, field_after):
    if field_before.piece is None and field_after.piece is not None:
        return field_after
    else:
        return field_before


def get_difference(board, board_2):
    fields = []
    for field in board.fields:
        for field2 in board_2.fields:
            if field.number == field2.number:
                if field.is_the_same_field_different(field2):
                    if field.piece is not None and field2.piece is None\
                            or field.piece is None and field2.piece is not None:
                        fields.append(field)
                        fields.append(field2)

    return fields


def try_to_get_move_category(fields):
    changes = []
    for i in range(0, len(fields), 2):
        smth = {"ID": fields[i].number, "WAS": fields[i].piece, "IS": fields[i + 1].piece}
        changes.append(smth)
        i += 1

    if was_this_regular_move(changes):
        print("REGULAR MOVE")
    elif was_this_regular_taking(changes):
        print("REGULAR TAKING")


def was_this_regular_move(changes):
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            beg_id = changes[s]["ID"]
            beg_piece = changes[s]["WAS"]
            for i in changes:
                if (i["ID"] == beg_id + 9 or i["ID"] == beg_id + 7 or i["ID"] == beg_id - 9 or i["ID"] == beg_id - 7)\
                        and i["WAS"] is None and beg_piece == i["IS"]:
                    return True
    return False


def was_this_regular_taking(changes):
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            beg_id = changes[s]["ID"]
            beg_piece = changes[s]["WAS"]
            for i in changes:
                if (i["ID"] == beg_id + 18 or i["ID"] == beg_id + 14
                    or i["ID"] == beg_id - 18 or i["ID"] == beg_id - 14)\
                        and i["WAS"] is None and beg_piece == i["IS"]:
                    return True
    return False


if __name__ == '__main__':
    board0 = Board("plansza00.png")
    board1 = Board("plansza01.png")
    board2 = Board("plansza02.png")
    board3 = Board("plansza03.png")
    board4 = Board("plansza04.png")
    board5 = Board("plansza05.png")

    difference = get_difference(board0, board1)
    try_to_get_move_category(difference)
    difference = get_difference(board1, board2)
    try_to_get_move_category(difference)
    difference = get_difference(board2, board3)
    try_to_get_move_category(difference)
    difference = get_difference(board3, board4)
    try_to_get_move_category(difference)
    difference = get_difference(board4, board5)
    try_to_get_move_category(difference)