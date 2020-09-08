
from src.VisionModule import image_processing


class Field:
    def __init__(self, number=0, colour=None, piece=None, crown=False):
        self.colour = colour
        self.number = number
        self.crown = crown
        # self.piece = piece
        if piece == 'COLOR_BOT':
            self.piece = 'BLACK'
        elif piece == 'COLOR_TOP':
            self.piece = 'WHITE'
        else:
            self.piece = None

    def set_colour(self, colour):
        self.colour = colour

    def set_piece(self, piece):
        self.piece = piece

    def is_the_same_field_different(self, field):
        if field.number == self.number:
            if field.piece != self.piece:
                if (field.piece is None and self.piece is not None) \
                        or (field.piece is not None and self.piece is None):
                    return True
                elif field.piece == self.piece:
                    return False
        else:
            raise Exception("Not the same field!")

    def __str__(self):
        return "{" + \
               "\n  Number: " + str(self.number) + \
               ",\n  Colour: " + str(self.colour) + \
               ",\n  Piece: " + str(self.piece) + \
               "\n}"

    def __eq__(self, other):
        return isinstance(other, Field) \
               and other.piece == self.piece \
               and other.colour == self.colour \
               and other.number == self.piece


class Board:
    is_taking_required = False
    taking_required = ""
    previous_move = "BLACK"

    def __init__(self, image_name):
        self.fields = []
        board_from_image = image_processing.run_test(image_name)

        for field in board_from_image:
            number = field["ID"]
            colour = field["Field"]
            piece = field["Piece"]
            crown = field["Crown"]
            self.fields.append(Field(number, colour, piece, crown))

    # debug only
    def validate_initially(self, full_game=False):
        black_counter = 0
        white_counter = 0
        field_counter = 0

        for field in self.fields:
            if field.piece == 'BLACK':
                black_counter += 1
            elif field.piece == 'WHITE':
                white_counter += 1
            field_counter += 1

        if black_counter + white_counter < 24 and full_game:
            raise Exception("Wrong amount of draughts")
        if field_counter < 64:
            raise Exception("Wrong amount of fields")

    def validate_placement(self):
        for field in self.fields:
            if field.piece is not None and field.colour == 'WHITE':
                raise Exception("Draught placed on wrong field! \n" + str(field))

    def get_blacks(self):
        counter = 0
        for field in self.fields:
            if field.piece == 'BLACK':
                counter += 1
        return counter

    def get_whites(self):
        counter = 0
        for field in self.fields:
            if field.piece == 'WHITE':
                counter += 1
        return counter


if __name__ == '__main__':
    board = Board("planszafullWRONG.png")

    try:
        board.validate_initially(True)
    except Exception as e:
        print("***************")
        print(str(e))
        print("***************")

    # for c in board.fields:
    #     print(c)
