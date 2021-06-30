import uuid

class Player:
    def __init__(self):
        self.identifier = str(uuid.uuid4())
        self.cards = []

    def draw_card(self, cards):
        self.cards = cards
