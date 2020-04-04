
from src.VisionModule import image_utils
from src.VisionModule.image_utils import ImageProcessor


class Field:
    def __init__(self, number=0, colour=None, piece=None):
        self.colour = colour
        self.number = number
        # self.piece = piece
        if piece == 'CAT#2':
            self.piece = 'BLACK'
        elif piece == 'CAT#1':
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
                elif 'CAT' in field.piece and 'CAT' in self.piece:
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
        return isinstance(other, Field)\
               and other.piece == self.piece\
               and other.colour == self.colour\
               and other.number == self.piece

class Board:
    def __init__(self, image_name):
        self.fields = []
        img_proc = ImageProcessor()
        image = img_proc.load_image(image_name)
        image = img_proc.resize(16, image)
        board_from_image = img_proc.iterate_through_image(image)

        for field in board_from_image:
            number = field["ID"]
            data = field["DATA"]
            piece = None
            colour = None
            for datum in data:
                if 'PIECE' in datum:
                    piece = datum.get("PIECE", None)
                if 'Field' in datum:
                    colour = datum.get("Field", {})
            self.fields.append(Field(number, colour, piece))

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
