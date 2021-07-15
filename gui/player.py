import time


class Player():
    def __init__(self, id, cards, status):
        self.time_limit = 60
        self.id = id
        self.cards = cards
        self.status = status
        self.start_time = time.time()
        self.timer = 60

    def update_time(self):
        elapsed_time = time.time() - self.start_time
        self.timer = self.time_limit - int(elapsed_time)

    def is_time_out(self):
        return self.timer <= 0
