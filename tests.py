import pytest
from collections import Counter
from helper_functions import (
    get_shuffled_deck,
    split_deck,
    map_card_to_numeric,
    compare_cards,
)

from war_game import play_round
from schemas import Player


def test_even_deck_length():
    deck = [1, 2, 3, 4]
    hand1, hand2 = split_deck(deck)
    assert len(hand1) == len(hand2)


def test_no_overlap_unique_values():
    deck = [1, 2, 3, 4]
    hand1, hand2 = split_deck(deck)
    assert len(set(hand1) & set(hand2)) == 0


def test_odd_deck_player2_has_one_more():
    deck = [1, 2, 3]
    hand1, hand2 = split_deck(deck)
    assert len(hand2) == len(hand1) + 1


def test_deck_length():
    deck = get_shuffled_deck()
    assert len(set(deck)) == 52, "Deck should have 52 unique cards"


def test_four_of_each_number():
    deck = get_shuffled_deck()
    values = [card[:-1] for card in deck]
    values_counter = Counter(values)
    expected_values = list(map(str, range(2, 11))) + ["A", "J", "Q", "K"]
    for value in expected_values:
        assert values_counter[value] == 4


def test_thirteen_of_each_suit():
    deck = get_shuffled_deck()
    suits_counter = Counter(card[-1] for card in deck)
    for suit in ("c", "d", "h", "s"):
        assert suits_counter[suit] == 13


def test_map_card_to_numeric():
    assert map_card_to_numeric("Joker") == 0
    assert map_card_to_numeric("Jc") == 11
    assert map_card_to_numeric("Qs") == 12
    assert map_card_to_numeric("Kh") == 13
    assert map_card_to_numeric("2d") == 2
    assert map_card_to_numeric("Ah") == 14


def test_invalid_card_raises_exception():
    with pytest.raises(ValueError):
        map_card_to_numeric("Xh")


def test_same_cards():
    """Test when both cards have the same value."""
    assert compare_cards("2h", "2h") == 0
    assert compare_cards("Kc", "Kd") == 0
    assert compare_cards("10s", "10c") == 0


def test_card1_greater():
    """Test when card_1 has higher value than card_2."""
    assert compare_cards("Ah", "Kh") == 1
    assert compare_cards("10d", "2d") == 1
    assert compare_cards("Js", "9s") == 1


def test_card1_lesser():
    """Test when card_1 has lower value than card_2."""
    assert compare_cards("2c", "3c") == 2
    assert compare_cards("Qh", "Kh") == 2
    assert compare_cards("10s", "As") == 2


def test_suit_up_active_same_suit():
    """Test when suit_up is active and cards have the same suit."""
    assert compare_cards("2h", "5h", suit_up_active=True) == 3
    assert compare_cards("Ac", "10c", suit_up_active=True) == 3
    assert compare_cards("Js", "Qs", suit_up_active=True) == 3


def test_suit_up_active_different_suit():
    """Test when suit_up is active but cards have different suits."""
    assert compare_cards("2h", "5c", suit_up_active=True) == 2
    assert compare_cards("Ac", "10d", suit_up_active=True) == 1


def test_same_value_different_suit():
    """Test when cards have same value but different suits with suit_up inactive."""
    assert compare_cards("2h", "2c") == 0
    assert compare_cards("As", "Ad") == 0


def test_same_value_same_suit():
    """Test when cards have same value and same suit."""
    assert compare_cards("2h", "2h") == 0
    assert compare_cards("2h", "2h", suit_up_active=True) == 0


def test_player_initialization():
    player = Player(hand=["2h", "2c"])
    assert player.hand == ["2h", "2c"]
    assert player.discard == []
    assert player.played_cards == []

    player = Player(hand=["As"], discard=["Ad"], played_cards=["2h"])
    assert player.hand == ["As"]
    assert player.discard == ["Ad"]
    assert player.played_cards == ["2h"]


def test_no_cards_property():
    player = Player(hand=["As", "Ad"])
    assert player.no_cards is False

    player = Player(hand=[], discard=["As"])
    assert player.no_cards is False

    player = Player(hand=[], discard=[])
    assert player.no_cards is True


def test_refill_hand():
    player = Player(hand=[], discard=["As", "Ad"])
    with pytest.raises(AttributeError):
        player.__refill_hand()


def test_play_card_from_top():
    player = Player(hand=["As", "2s", "3s"])
    player.play_card()
    assert player.hand == ["As", "2s"]
    assert player.played_cards == ["3s"]

    player = Player(hand=["As"], discard=[])
    player.play_card()
    assert player.hand == []
    assert player.played_cards == ["As"]


def test_play_card_from_bottom():
    # Test playing from bottom
    player = Player(hand=["As", "2s", "3s"])
    player.play_card(from_bottom=True)
    assert player.hand == ["2s", "3s"]
    assert player.played_cards == ["As"]


def test_play_card_with_refill():
    # Test playing when hand is empty but discard has cards
    player = Player(hand=[], discard=["As", "2s", "3s"])
    player.play_card()
    assert player.hand == [
        "3s",
        "2s",
    ]
    assert player.discard == []
    assert player.played_cards == ["As"]

    player = Player(hand=[], discard=["As", "2s", "3s"])
    player.play_card(from_bottom=True)
    assert player.hand == ["2s", "As"]
    assert player.discard == []
    assert player.played_cards == ["3s"]
