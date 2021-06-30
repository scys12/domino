import random

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
    ]

    def __init__(self):
        """
        2 Player card list and first card
        """
        self.player1_cards = []
        self.player2_cards = []
        self.firstCard = None
        self.current_turn = "player1"

    def serialize_data(self):
      return {
        'first_card' : self.player1_cards,
        'second_card' : self.player2_cards,
        'current_turn' : self.current_turn,
      }
  
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