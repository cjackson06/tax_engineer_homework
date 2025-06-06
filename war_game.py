import logging
import argparse
from helper_functions import (
    compare_cards,
    get_shuffled_deck,
    split_deck,
)
from typing import Optional
from schemas import Player

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[],
)
logger = logging.getLogger()


def play_round(
    player1: Player,
    player2: Player,
    deal: int = 1,
    from_bottom: bool = False,
    suit_up_active: bool = False,
    auto_play: bool = False,
    output: str | bool = False,
) -> Optional[int]:
    """
    Single round of gameplay, wars are considered part of the same round, and are recursively called
    """
    if (not auto_play) and (not output):
        input("Press Enter to play")

    for _ in range(0, deal):
        if player1.no_cards and player2.no_cards:
            # Players have played all cards in one long series of wars, just compare on the last card or draw
            # assume suit_up can't activate on this last hand
            return compare_cards(
                player1.played_cards[-1],
                player2.played_cards[-1],
                suit_up_active=False,
            )

        # You lose if you don't have enough cards for deal
        if player1.no_cards:
            "Player 2 wins, player 1 has no cards left"
            return 2
        if player2.no_cards:
            "Player 1 wins, player 2 has no cards left"
            return 1

        player1.play_card(from_bottom)
        player2.play_card(from_bottom)

    comparison = compare_cards(
        player1.played_cards[-1],
        player2.played_cards[-1],
        suit_up_active=(suit_up_active and deal != 4),
    )  # check if deal is 4, if it is it's a regular war and you can't enter suit-up

    logger.info(
        f"P1: H:{str(len(player1.hand)).ljust(2)} | D:{str(len(player1.discard)).ljust(2)} | {player1.played_cards}{'*' if comparison == 1 else ' '}"
    )
    logger.info(
        f"P2: H:{str(len(player2.hand)).ljust(2)} | D:{str(len(player2.discard)).ljust(2)} | {player2.played_cards}{'*' if comparison == 2 else ' '}"
    )

    spoils_of_war = player1.played_cards + player2.played_cards
    if comparison == 1:
        player1.discard += spoils_of_war
    elif comparison == 2:
        player2.discard += spoils_of_war
    elif comparison == 0:
        logger.info("War!")
        return play_round(
            player1=player1,
            player2=player2,
            deal=4,
            from_bottom=False,
            suit_up_active=False,
            auto_play=auto_play,
            output=output,
        )
    elif comparison == 3:
        logger.info("Suit Up!")
        return play_round(
            player1=player1,
            player2=player2,
            deal=2,
            from_bottom=True,
            suit_up_active=True,
            auto_play=auto_play,
            output=output,
        )

    return None  # no winner yet


def play_war(
    auto_play: bool = False, suit_up: bool = False, output: str | bool = False
):
    """
    Play game
    """

    # setup deck and player data objects
    deck = get_shuffled_deck()
    player_1_hand, player_2_hand = split_deck(deck)
    player1 = Player(hand=player_1_hand)
    player2 = Player(hand=player_2_hand)
    round = 1

    while round < 10000:
        player1.played_cards, player2.played_cards = [], []
        logger.info(f"---- Round {round} ----")
        winner = play_round(
            player1,
            player2,
            deal=1,
            suit_up_active=suit_up,
            auto_play=auto_play,
            output=output,
        )
        if winner:
            logger.info(f"Player {winner} Wins in {round} rounds!")
            break
        elif winner == 0:  # for rare case
            logger.info("Draw!")
            break

        # move cards from discard to hand if hand is empty
        player_2_wins = player1.no_cards
        if player_2_wins:
            logger.info(f"Player 2 Wins in {round} rounds!")
            break

        player_1_wins = player2.no_cards
        if player_1_wins:
            logger.info(f"Player 1 Wins in {round} rounds!")
            break

        round += 1

    else:
        raise Exception("Suspected infitine loop. Ending game.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Prevent request for user action, move game along automatically",
    )
    parser.add_argument(
        "--output",
        nargs="?",
        const="gameplay.log",
        default=False,
        help="Auto play game and output the game results to a log file",
    )
    parser.add_argument(
        "--suit-up", action="store_true", help='run game with "suit up" house rule'
    )
    args = parser.parse_args()
    if args.output:
        logger.addHandler(
            logging.FileHandler(
                mode="w", filename=(args.output.replace(".log", "") + ".log")
            )
        )
    else:
        logger.addHandler(logging.StreamHandler())
    play_war(auto_play=args.auto, suit_up=args.suit_up, output=args.output)
