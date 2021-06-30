import uuid


class Player:
    def __init__(self, connect):
        self.identifier = str(uuid.uuid4())
        self.cards = []
        self.connect = connect
        self.last_throwed = None

    def draw_card(self, cards):
        self.cards = cards

    def throw_card(self, cards_position):
        self.last_throwed = self.cards[cards_position]
        del self.cards[cards_position]      