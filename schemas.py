from pydantic import BaseModel


class Player(BaseModel):
    hand: list[str]
    discard: list[str] = []
    played_cards: list[str] = []

    @property
    def no_cards(self):
        return len(self.hand) + len(self.discard) == 0

    def __refill_hand(self):
        if len(self.hand) > 0:
            return None
        self.discard.reverse()
        self.hand = self.discard.copy()
        self.discard.clear()
        return None

    def play_card(self, from_bottom: bool = False):
        if len(self.hand) == 0:
            self.__refill_hand()

        self.played_cards.append(self.hand.pop(0 if from_bottom else -1))
        return None
