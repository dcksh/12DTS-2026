# card dealer
# stores a deck of cards, deals a hand of any number 1-52, and describes each card with the colour, value, and suit
# e.g. Red Queen of Hearts

# daksh
# 19/2/26

# modules
import random

# variables
card_deck = []
card_number = 0
again = 0
# loops to use for error testing later
card_loop = True
start_loop = True
again_loop = True


# constants
SUIT = ["Hearts", "Diamonds", "Clubs", "Spades"]
FACES = ["Jack", "Queen", "King"]

# functions
def new_deck(): # makes new deck
    card_deck.clear() # to clear any previous remaining cards
    for i in range(1, 12): # cards 1-11
        for j in range(0, 4): # for the different suits heart - spade
            if i > 10: # if > 10, face cards start to print
                for k in range(0, 3): # makes 4 instances of each face card with each suit
                    card_deck.append([FACES[k], SUIT[j]])
            else: # if not face card, add normal card with suit
                card_deck.append([i, SUIT[j]])


def hand_deal(amount): # deals you the hand
    print(" -- DECK --")
    for i in range(0, amount): # range for the amount of times you want a card
        card = (random.randint(1, len(card_deck))) - 1
        if card_deck[card][1] == "Hearts" or card_deck[card][1] == "Diamonds":
            colour = "Red" # so you can describe card well
        else:
            colour = "Black"
        print(colour, card_deck[card][0], "of", card_deck[card][1]) # e.g. Red Queen of Hearts
        card_deck.pop(card) # removes card to avoid duplicates


# ------------------------------- main module -------------------------------
while start_loop == True: # to use if user wants to go again
    new_deck()
    print(" -- DEALER --")
    print("Welcome to the dealer!")
    print("Please select the amount of cards you want to deal.")
    # loops now = true so error loops stay up
    card_loop = True
    again_loop = True
    start_loop = False # we dont want to start the entire thing again without user's consent
    while card_loop == True:
        try: # error catching
            card_number = int(input())
            if card_number > 0 and card_number <= 52: # check to see if its 1-52 (no more than 52 in a deck)
                hand_deal(card_number)
                card_loop = False
            else:
                print("Please enter a valid integer from 1 - 52.")
        except ValueError:
            print("Please enter a valid integer from 1 - 52.")
    while again_loop == True:
        print("------------")
        print("Do you want to go again? (Yes/No)")
        again = input().lower()
        if again == "yes":
            start_loop = True
            again_loop = False
        elif again == "no":
            again_loop = False
        else:
            print("Please either say 'Yes' or 'No'!")