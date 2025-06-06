from pydantic import BaseModel


class Player(BaseModel):
    hand: list[str]
    discard: list[str] = []
    played_cards: list[str] = []

    @property
    def no_cards(self):
        return len(self.hand) + len(self.discard) == 0

    def refill_hand(self):
        if len(self.hand) > 0:
            return None
        self.discard.reverse()
        self.hand = self.discard.copy()
        self.discard.clear()
        return None
