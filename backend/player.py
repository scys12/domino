import uuid


class Player:
    def __init__(self, connect):
        self.identifier = str(uuid.uuid4())
        self.cards = []
        self.connect = connect
        self.last_throwed = None
        self.status = None

    def draw_card(self, cards):
        self.cards = cards

    def throw_card(self, top, down):
        print(self.cards)
        print((top, down))
        self.cards.remove((top, down))

    def set_player_status(self, status):
        self.status = status

    def serialize_data(self):
        return {
            'id': self.identifier,
            'cards': self.cards,
            'last_throwed': self.last_throwed,
            'status': self.status,
        }
