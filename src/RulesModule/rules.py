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
                    if field.piece is not None and field2.piece is None \
                            or field.piece is None and field2.piece is not None:
                        fields.append(field)
                        fields.append(field2)

    return fields


def check_if_taking_required(board_2, move_made, previous_move):
    Board.who_has_to_take = []
    Board.is_taking_required = False
    Board.taking_required = []
    # for whites
    fields_amount = len(board_2.fields)
    for i in range(0, fields_amount):
        if board_2.fields[i].piece == "WHITE":
            if not (i + 14 > fields_amount or (i + 7) % 8 == 1) and board_2.fields[i + 14].colour is "Black":
                if board_2.fields[i + 7].piece == "BLACK" and board_2.fields[i + 14].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i + 14)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('WHITE')
            if not (i + 18 > fields_amount or (i + 9) % 8 == 0) and board_2.fields[i + 18].colour is "Black":
                if board_2.fields[i + 9].piece == "BLACK" and board_2.fields[i + 18].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i + 18)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('WHITE')
            if not (i - 18 < 1 or (i - 9) % 8 == 1) and board_2.fields[i - 18].colour is "Black":
                if board_2.fields[i - 9].piece == "BLACK" and board_2.fields[i - 18].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i - 18)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('WHITE')
            if not (i - 14 < 1 or (i - 7) % 8 == 0) and board_2.fields[i - 14].colour is "Black":
                if board_2.fields[i - 7].piece == "BLACK" and board_2.fields[i - 14].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i - 14)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('WHITE')
    # for blacks
    for i in range(0, fields_amount):
        if board_2.fields[i].piece == "BLACK":
            if not (i + 14 >= fields_amount or (i + 7) % 8 == 1) and board_2.fields[i + 14].colour is "Black":
                if board_2.fields[i + 7].piece == "WHITE" and board_2.fields[i + 14].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i + 14)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('BLACK')
            if not (i + 18 >= fields_amount or (i + 9) % 8 == 0) and board_2.fields[i + 18].colour is "Black":
                if board_2.fields[i + 9].piece == "WHITE" and board_2.fields[i + 18].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i + 18)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('BLACK')
            if not (i - 18 < 1 or (i - 9) % 8 == 1) and board_2.fields[i - 18].colour is "Black":
                if board_2.fields[i - 9].piece == "WHITE" and board_2.fields[i - 18].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i - 18)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('BLACK')
            if not (i - 14 < 1 or (i - 7) % 8 == 0) and board_2.fields[i - 14].colour is "Black":
                if board_2.fields[i - 7].piece == "WHITE" and board_2.fields[i - 14].piece is None:
                    Board.taking_required.append(str(change_id_to_normal(i)) + "x" + str(change_id_to_normal(i - 14)))
                    Board.is_taking_required = True
                    Board.who_has_to_take.append('BLACK')

    # checking if the next turn should consist of taking
    if Board.is_taking_required and Board.previous_move in Board.who_has_to_take and "x" in move_made:
        Board.taking_required = True
    elif Board.is_taking_required and Board.previous_move not in Board.who_has_to_take:
        Board.is_taking_required = True



def get_who_made_the_move(changes, move_made):
    if move_made.__contains__("x"):
        ids = move_made.split("x")
    else:
        ids = move_made.split("-")
    for i in range(0, len(changes)):
        if str(change_id_to_normal(changes[i]["ID"])) in ids and changes[i]["WAS"] is not None:
            return changes[i]["WAS"]
        elif str(change_id_to_normal(changes[i]["ID"])) in ids and changes[i]["IS"] is not None:
            return changes[i]["IS"]


def try_to_get_move_category(board_1, board_2):
    fields = get_difference(board_1, board_2)
    changes = []
    taken_id = 0
    for i in range(0, len(fields), 2):
        smth = {"ID": fields[i].number, "WAS": fields[i].piece, "IS": fields[i + 1].piece}
        changes.append(smth)
        i += 1
    move_made = ""
    if was_this_regular_move(changes):
        print("REGULAR MOVE")
        move_made = print_regular_move_pgn(changes)
        previous_move = Board.previous_move
        who_made_the_move = get_who_made_the_move(changes, move_made)
        if who_made_the_move == previous_move\
                or (Board.is_taking_required and who_made_the_move in Board.who_has_to_take):
            raise Exception("Not your turn", "Move: " + move_made,
                            "Moved: " + who_made_the_move,
                            "Previous move: " + previous_move,
                            "Was taking required: " + str(Board.is_taking_required))
        Board.previous_move = who_made_the_move
        check_if_taking_required(board_2, move_made, previous_move)
    elif was_this_regular_taking(changes):
        print("REGULAR TAKING")
        move_made = print_regular_taking_pgn(changes)
        taken_id = get_taken_id(changes, move_made)
        previous_move = Board.previous_move
        who_made_the_move = get_who_made_the_move(changes, move_made)
        if who_made_the_move == previous_move or not Board.is_taking_required:
            if not(who_made_the_move == previous_move and Board.is_taking_required):
                raise Exception("Not your turn", "Move: " + move_made,
                                "Moved: " + who_made_the_move,
                                "Previous move: " + previous_move,
                                "Was taking required: " + str(Board.is_taking_required))
        Board.previous_move = who_made_the_move
        check_if_taking_required(board_2, move_made, previous_move)
    return {"player": Board.previous_move, "move": move_made, "captured": taken_id}


def get_taken_id(changes, move):
    taken_id = 0
    ids = move.split("x")
    for i in range(0, len(changes)):
        if changes[i]["WAS"] is not None and changes[i]["IS"] is None and str(
                change_id_to_normal(changes[i]["ID"])) not in ids:
            taken_id = changes[i]["ID"]
    return change_id_to_normal(taken_id)


def print_regular_move_pgn(changes):
    id2 = change_id_to_normal(changes[1]["ID"])
    id1 = change_id_to_normal(changes[0]["ID"])

    if changes[0]["WAS"] is not None:
        to_print = str(int(id1)) + "-" + str(int(id2))
    else:
        to_print = str(int(id2)) + "-" + str(int(id1))

    print(to_print)
    return to_print


def change_id_to_normal(field_id):
    upd_id = field_id + 1
    if upd_id % 2 != 0:
        return int(upd_id // 2) + 1
    else:
        return int(upd_id / 2)


def print_regular_taking_pgn(changes):
    to_print = ""
    id3 = change_id_to_normal(changes[2]["ID"])
    id2 = change_id_to_normal(changes[1]["ID"])
    id1 = change_id_to_normal(changes[0]["ID"])

    if changes[0]["WAS"] is not None:
        if changes[1]["IS"] == changes[0]["WAS"]:
            to_print = str(int(id1)) + "x" + str(int(id2))
        elif changes[2]["IS"] == changes[0]["WAS"]:
            to_print = str(int(id1)) + "x" + str(int(id3))
        else:
            if changes[1]["IS"] is None:
                to_print = str(int(id2)) + "x" + str(int(id3))
            else:
                to_print = str(int(id3)) + "x" + str(int(id2))
    else:
        if changes[1]["WAS"] == changes[0]["IS"]:
            to_print = str(int(id2)) + "x" + str(int(id1))
        elif changes[2]["WAS"] == changes[0]["IS"]:
            to_print = str(int(id3)) + "x" + str(int(id1))

    print(to_print)
    return to_print


def was_this_regular_move(changes):
    if len(changes) != 2:
        return False
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            beg_id = changes[s]["ID"]
            beg_piece = changes[s]["WAS"]
            for i in changes:
                if (i["ID"] == beg_id + 9 or i["ID"] == beg_id + 7 or i["ID"] == beg_id - 9 or i["ID"] == beg_id - 7) \
                        and i["WAS"] is None and beg_piece == i["IS"]:
                    return True
    return False


def was_this_regular_taking(changes):
    if len(changes) != 3:
        return False
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            beg_id = changes[s]["ID"]
            beg_piece = changes[s]["WAS"]
            for i in changes:
                if (i["ID"] == beg_id + 18 or i["ID"] == beg_id + 14
                    or i["ID"] == beg_id - 18 or i["ID"] == beg_id - 14) \
                        and i["WAS"] is None and beg_piece == i["IS"]:
                    return True
    return False


def was_this_multiple_taking(changes):
    kill_count = 0
    begin_point = None
    end_point = None
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            kill_count = kill_count + 1
        elif changes[s]["WAS"] is None and changes[s]["IS"] is not None:
            end_point = changes[s]
    for s in range(0, len(changes)):
        if changes[s]["WAS"] == end_point["IS"]:
            begin_point = changes[s]
    if kill_count > 2 and begin_point is not None and end_point is not None:
        return True
    else:
        return False


def print_multi_taking(changes):
    to_print = ""
    kill_count = 0
    begin_point = None
    end_point = None
    for s in range(0, len(changes)):
        if changes[s]["WAS"] is not None and changes[s]["IS"] is None:
            kill_count = kill_count + 1
        elif changes[s]["WAS"] is None and changes[s]["IS"] is not None:
            end_point = changes[s]
    for s in range(0, len(changes)):
        if changes[s]["WAS"] == end_point["IS"]:
            begin_point = changes[s]

    to_print = str(change_id_to_normal(begin_point["ID"])) + "x" + str(change_id_to_normal(end_point["ID"]))
    print(to_print)


if __name__ == '__main__':
    prefix = "newtest2/"
    suffix = ".png"
    name = "000"
    previous_board = Board(prefix + "000" + suffix)
    next_board = Board(prefix + "001" + suffix)
    previous_board.validate_initially(True)
    j = 2
    while j < 38:
        try_to_get_move_category(previous_board, next_board)
        previous_board = next_board
        next_board = Board(prefix + str(j).zfill(3) + suffix)
        j = j + 1
