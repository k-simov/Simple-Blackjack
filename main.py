import random
from time import sleep

# Card constants
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
}


def create_deck():
    return [f"{rank} of {suit}" for rank in RANKS for suit in SUITS]


def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


def get_card_value(card):
    return RANK_VALUES[card.split()[0]]


def calculate_score(cards):
    score = sum(get_card_value(card) for card in cards)
    aces = sum(1 for card in cards if card.startswith('A'))
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


def get_player_info():
    while True:
        name = input("Please input your name: ")
        while True:
            chips = input("Please input the chips you start with: ")
            if chips.isdigit():
                chips = int(chips)
                break
            print("You gave an invalid value.")

        print(f"You are named {name} and you start with {chips} chips.")
        if input("Enter 'Change' if you want to change that: ").lower().strip() != 'change':
            return name, chips


def get_bet(chips):
    while True:
        bet = input(f"Please input your bet. You have {chips} chips: ")
        if bet.isdigit() and 0 < int(bet) <= chips:
            return int(bet)
        print("The given value must be more than 0 and less than or equal to your chips.")


def play_round(deck, player_chips):
    bet = get_bet(player_chips)
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]

    print("Dealer's hand:")
    print("Face down card")
    print(dealer_hand[1])
    print("Your hand:")
    for card in player_hand:
        print(card)

    # Player's turn
    while True:
        if input("Type 'h' to hit or 's' to stand: ").lower().strip() == 'h':
            player_hand.append(draw_card(deck))
            print(f"You have drawn a {player_hand[-1]}")
            if calculate_score(player_hand) > 21:
                print("You went bust.")
                return -bet
        else:
            break

    # Dealer's turn
    print("Dealer's hand:")
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))
    for card in dealer_hand:
        print(card)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    print(f"Your score is {player_score} and the dealer's score is {dealer_score}.")

    if dealer_score > 21:
        print("The dealer went bust. You win!")
        return bet * 2.5 if player_score == 21 else bet
    elif player_score > dealer_score:
        print("You win!")
        return bet * 2.5 if player_score == 21 else bet
    elif player_score == dealer_score:
        print("It's a tie!")
        return 0
    else:
        print("You lost.")
        return -bet


def main():
    print("Hello, player.")
    sleep(1)
    player_name, player_chips = get_player_info()

    while player_chips > 0:
        deck = create_deck()
        player_chips += play_round(deck, player_chips)
        player_chips = round(player_chips)

        if player_chips <= 0:
            print('You have 0 chips and you lost the game.')
            break

        if input("Type 'exit' to quit or press Enter to play again: ").lower().strip() == 'exit':
            break

    print(f"Thank you for playing, {player_name}. You finished with {player_chips} chips.")


if __name__ == "__main__":
    main()
