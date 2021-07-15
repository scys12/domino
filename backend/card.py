class Card:
    def __init__(self, row, col, top, down, is_in_board, direction, position):
        self.row = row
        self.col = col
        self.top = top
        self.down = down
        self.is_in_board = is_in_board
        self.direction = direction
        self.position = position

    def serialize_data(self):
        return {
            "row": self.row,
            "col": self.col,
            "top": self.top,
            "down": self.down,
            "is_in_board": self.is_in_board,
            "direction": self.direction,
            "position": self.position,
        }
