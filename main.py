from time import sleep
import random

# initializing the deck
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
deck = [rank + " of " + suit for rank in ranks for suit in suits]
ranks_and_powers = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
}


# drawing a card function
def draw_a_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


# gets the card's power
def get_card_power(card):
    card_rank = card.split(' ')[0]  # Split the card string and get the rank part
    card_power = ranks_and_powers[card_rank]
    return card_power


# add up player score
def get_total_score(card_list):
    score = 0
    num_aces = 0
    for card in card_list:
        current_card = get_card_power(card)
        score += current_card
        if 'A' in card:
            num_aces += 1
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score


# Game start
print("Hello, player.")
sleep(1)
# Loop for value confirmation and changing
while True:
    player_name = input("Please input your name: ")

    while True:
        player_chips = input("Please input the chips you start with: ")
        if player_chips.isdigit():
            player_chips = int(player_chips)
            break
        else:
            print("You gave an invalid value.")

    print(f"You are named {player_name} and you start with {player_chips} chips."
          f"\nEnter \"Change\" if you want to change that: ")

    if not input().lower().strip() == 'change':
        break


# main game loop

while True:
    # init and reset variables
    temp_deck = deck.copy()
    dealer_cards = []
    player_cards = []
    player_bust = False
    dealer_bust = False
    # setting the bet
    while True:
        temp_variable = int(input(f"Please input your bet. You have {player_chips} chips: "))
        if player_chips >= temp_variable > 0:
            bet = temp_variable
            break
        else:
            print("The given value must be more than 0 and less than or equal to your chips. ")
    # game start
    sleep(1)
    print("Let's begin!")
    sleep(0.5)
    player_cards.append(draw_a_card(temp_deck))
    dealer_cards.append(draw_a_card(temp_deck))
    player_cards.append(draw_a_card(temp_deck))
    dealer_cards.append(draw_a_card(temp_deck))
    print("The dealer has the following cards: ")
    print("Face down card")
    print(dealer_cards[1])
    print("You have the following cards: ")
    for i in player_cards:
        print(i)
    # hit or stand loop until stand or bust
    while True:
        print("Do you want to hit or stand?")
        temp_variable = input("Type 'h' to hit or 's' to stand: ")
        temp_variable.strip().lower()
        if temp_variable == 'h':
            temp_variable = draw_a_card(temp_deck)
            player_cards.append(temp_variable)
            print("You have drawn a " + temp_variable)
        elif temp_variable == 's':
            break
        temp_variable = get_total_score(player_cards)
        # check if bust
        if temp_variable > 21:
            print("You went bust.")
            player_chips -= bet
            player_bust = True
            break



    if not player_bust:
        while get_total_score(dealer_cards) < 17:
            dealer_cards.append(draw_a_card(temp_deck))

        print("The dealer's cards are: ")
        for i in dealer_cards:
            print(i)

        player_score = get_total_score(player_cards)
        dealer_score = get_total_score(dealer_cards)

        print(f"Your score is {player_score} and the dealer's score is {dealer_score}.")
        if dealer_score > 21:
            dealer_bust = True
            print("The dealer went bust. You win!")
            if player_score == 21:
                print("You got a blackjack! You win X2.5 your bet.")
                player_chips += bet * 1.5
                player_chips = round(player_chips)
            else:
                player_chips += bet
        if not dealer_bust:
            if player_score > dealer_score:
                if player_score == 21:
                    print("You got a blackjack! You instantly win X2.5 your bet.")
                    player_chips += bet * 1.5
                    player_chips = round(player_chips)
                else:
                    print("You win!")
                    player_chips += bet
            else:
                print("You lost.")
                player_chips -= bet

    if player_chips <= 0:
        print('You have 0 chips and you lost the game.')
        break
    # Exit or replay
    if input("Type 'exit' if you want to exit or press 'Enter' to replay: ") == 'exit':
        break
