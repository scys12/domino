import random
from backend.card import Card


class Board:
    cards = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
        (3, 3),
        # (3, 4),
    ]

    def __init__(self):
        """
        2 Player card list and first card
        """
        self.player1_cards = []
        self.board = []
        self.player2_cards = []
        self.firstCard = None
        self.current_turn = "player1"
        self.middle_card = self.cards.pop(random.randrange(len(self.cards)))

    def update_board(self, card_data):
        self.update_turn()
        card = Card(card_data['row'], card_data['col'], card_data['top'], card_data['down'],
                    card_data['is_in_board'], card_data['direction'], card_data['position'])
        self.board[card_data['row']][card_data['col']] = card.serialize_data()

    def update_turn(self):
        if self.current_turn == "player1":
            self.current_turn = "player2"
        else:
            self.current_turn = "player1"

    def serialize_data(self, player_status):
        data = {
            'current_turn': self.current_turn,
            'middle_card': self.middle_card,
            'board': self.board
        }
        # count enemy card
        if player_status == "player1":
            data["total_enemy_card"] = len(self.player2_cards)
        elif player_status == "player2":
            data["total_enemy_card"] = len(self.player1_cards)
        return data

    def init_board(self):
        ROWS, COLS = 28, 18
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == ROWS//2-1 and col == COLS//2-1:
                    card = Card(
                        row, col, self.middle_card[0], self.middle_card[1], True, "top", "middle")
                    self.board[row].append(card.serialize_data())
                else:
                    self.board[row].append(0)

    def generate_card(self, first_turn):
        """
        Generate 2 player card and first card,
        first_turn indicates whoever will draw first
        """
        picked = []
        count = 0
        picked_turn = first_turn

        while True:
            if count == len(self.cards):
                break
            i = random.randrange(len(self.cards))
            if self.cards[i] not in picked:
                if(self.firstCard == None):
                    self.firstCard = self.cards[i]
                else:
                    if(picked_turn == "player1"):
                        self.player1_cards.append(self.cards[i])
                        picked_turn = "player2"
                    else:
                        self.player2_cards.append(self.cards[i])
                        picked_turn = "player1"

                count = count + 1
                picked.append(self.cards[i])
