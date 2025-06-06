import math
import random


def get_shuffled_deck() -> list:
    """
    Generate Standard 52 card deck, 1-10 / J / Q / K, with 4 different suits
    """
    SUITS = ("c", "d", "h", "s")
    CARDS = tuple(map(str, range(2, 11))) + ("A", "J", "Q", "K")
    deck = [card + suit for suit in SUITS for card in CARDS]
    random.shuffle(deck)
    return deck


def split_deck(deck: list) -> tuple[list, list]:
    """Give half a deck to each player
    player 2 get's larger pile if there are an odd number of cards
    """
    half_deck = len(deck) // 2
    player_1_hand = deck[:half_deck]
    player_2_hand = deck[half_deck:]
    return player_1_hand, player_2_hand


def map_card_to_numeric(card: str) -> int:
    """Turn String values of cards into numeric representations for comparison"""
    if card == "Joker":
        return 0

    VALUE_MAPPER = {"A": "14", "J": "11", "Q": "12", "K": "13"}
    value = card[:-1]
    try:
        return int(value)
    except ValueError:
        pass
    face_card_value = VALUE_MAPPER.get(value)
    if not face_card_value:
        raise ValueError(f"Unknown card: {card}")
    return int(face_card_value)


def compare_cards(card_1: str, card_2: str, suit_up_active: bool = False) -> int:
    """
    return
        0 if they're the same
        1 if card_1 is greater than card_2
        2 if card_1 is less than card_2
        3 if cards are the same suit, and playing 'suit_up'
    """
    numeric_1 = map_card_to_numeric(card_1)
    numeric_2 = map_card_to_numeric(card_2)
    if numeric_1 == numeric_2:
        return 0
    elif suit_up_active and (card_1[-1] == card_2[-1]):
        return 3
    elif numeric_1 > numeric_2:
        return 1
    elif numeric_1 < numeric_2:
        return 2
    raise Exception(f"Comparison detected something unexpected: {card_1} vs. {card_2}")
