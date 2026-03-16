# balatro
# roguelike game where you score hands to beat blinds, and grab jokers to upgrade your hands against stronger blinds.
# 2.7 dts assessment
# daksh shah
# 10/3/26

# last updated - 10/3/26

# // STORY //
# Follows the story of Astus, a Jester from Ancient Rome.

# !! SO FAR !!
# - Deals a hand to the user
# - User may either sort the cards by rank/suit or select cards to play/discard
# - ** So far only testing the play :(

# modules
import random
import time

# variables
card_deck = []
hand = []
card_number = 0

anti = 0
blind = 0
boss_hp = 0
order_state = 1

# loops to use for error testing later
game_loop = True
choice_loop = True
card_selection_loop = True

# constants
SUIT = ["Hearts", "Diamonds", "Clubs", "Spades"]
CARDS = ["Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]
FACE_INITIALS = ["J, Q, K, A"]
POKER_HANDS = {
    "High Card" : [5,1],
    "Pair" : [10,2],
    "Two Pair" : [20,2],
    "Three of a Kind" : [30,3],
    "Straight" : [30,4],
    "Flush" : [35,4],
    "Full House" : [40,40],
    "Four of a Kind" : [60,7],
    "Straight Flush" : [100,8],
    "Royal Flush" : [100,8],
    "Five of a Kind" : [120,12],
    "Flush House" : [140,14],
    "Flush Five" : [160,16]
} # multipliers for each hand - stored by chip addition, then chip multiplier
BLIND_BASE_CHIPS = [300, 800, 2000, 5000, 11000, 20000, 35000, 50000] # scores for each anti, base chips increase per anti
BLIND_MULTIPLIERS = [[1,"Small"],[1.5,"Big"],[2,"Boss"]] # multiplier based on boss
HAND_SIZE = 32
SELECT_HAND_SIZE = 6

# functions
def blind_maker(): # makes the current blind
    global anti
    global boss_hp
    global blind

    blind += 1 # increases the blind each time, everytime it hits 3 resets to 1 and adds 1 to anti
    anti += 1 ## ^^^ PLEASE MAKE THIS

    boss_hp = BLIND_BASE_CHIPS[anti - 1]*BLIND_MULTIPLIERS[blind-1][0] # hp is set on the anti and blind, using the base chips and multipliers above
    print("Anti",anti)
    print(BLIND_MULTIPLIERS[blind-1][1],"Blind")
    print("Score:",boss_hp)
    print()


def new_deck(): # makes a new deck
    card_deck.clear() # clear old usae
    for i in range(1, 10): # prints out the number cards, uses for loops to make 44 of these
        for j in range(4):
            card_deck.append([SUIT[j], CARDS[i - 1], i+1, i+1])
    for k in range(9, 13): # same as above but face cards + ace
        for j in range(4):
            if k == 12:
                card_deck.append([SUIT[j], CARDS[k], 11, k + 2]) # different for ace as ace has 11 points.
            else:
                card_deck.append([SUIT[j], CARDS[k], 10, k+2])
    print(card_deck) # DEBUG


def hand_deal(amount): # deals you the hand
    print(" -- HAND --")
    for i in range(0, amount): # range for the amount of times you want a card
        card = (random.randint(1, len(card_deck))) - 1
        hand.append(card_deck[card])
        card_deck.pop(card) # removes card to avoid duplicates
    hand.sort(key=lambda x: (x[3],[0])) # sorts the stuff automatically by value of card, lowest to highest followed by alphabetical order of suits
    # lambda is a key you can use for your sort function to do stuff like this ^^
    order_state = 1 # state of ordering, can order by value first or suit first (changed later)
    for j in range(0,amount): # prints current hand
        hand[j].append(j+1)
        print(hand[j][4],hand[j][1],"of",hand[j][0])


def gameplay(): # main gameplay loop
    # local variables and loops
    global order_state
    selection_list = []
    chosen_cards = []
    chips = []

    game_loop = True
    choice_loop = True
    card_selection_loop = True

    while game_loop == True: # main game loop begin
        while choice_loop == True: # choice to either resort or select to play/refresh
            print()
            print("Enter 1 to switch sort between 'by number' and 'by suit', Enter 2 to select cards.")
            choice = input()
            if choice == "1": # sort
                if order_state == 1: # if by number, do suit
                    hand.sort(key=lambda x: (x[0], [3]))
                    order_state = 2
                elif order_state == 2: # opposite of above
                    hand.sort(key=lambda x: (x[3], [0]))
                    order_state = 1
                for j in range(0, len(hand)): # prints out the new sorting order, loop doesnt end as they have to play first
                    print(hand[j][4], hand[j][1], "of", hand[j][0])

                time.sleep(1)
            elif choice == "2": # chosen to select
                choice_loop = False
                while card_selection_loop == True:
                    try:
                        print("Please select the cards you want to play. (E.g. 1 3 5 7)")
                        cards_chosen = input()
                        for i in cards_chosen.split(" ",SELECT_HAND_SIZE-1):
                            # what this code does is takes the input e.g. "1 2 3" and seperates it into different elements in a list, each element ending at the space from " ".
                            # strip then gets rid of extra stuff (white spaces by default) to leave it as the number alone, allowing the code to convert it into an integer
                            # then, just adds it to the list fo selected cards
                            selection_list.append(int(i.strip()))

                    except ValueError: # error fixing
                        print()
                        print("Please enter a max of",SELECT_HAND_SIZE,"cards, and refer to the number at the start!")
                        print("E.g. if you want to pick '8 Queen of Hearts', please enter in 8, followed by the other cards you'd like!")
                        print()
                        selection_list.clear() # clears as even upon error the append happens sometimes (depending on the error), so clear it to make ti easy

                    # code to now place these selected cards into another list of chosen cards to play
                    # this code checks the order of the card in the hand, and compares it to the number the player chose and then looks for the right card
                    # after finding the card, it adds it to the list and moves on to look for the next card
                    if len(selection_list) > SELECT_HAND_SIZE or len(selection_list) < 1:
                        print("Please pick up to",SELECT_HAND_SIZE,"cards!")
                    else:
                        for i in range(0, len(selection_list)):
                            finding_card_loop = True
                            while finding_card_loop == True:
                                for j in range(0,len(hand)):
                                    find_chosen_card = hand[j][4]
                                    if find_chosen_card == selection_list[i]:
                                        chosen_cards.append(hand[j])
                                        finding_card_loop = False
                        card_selection_loop = False
                score_calculation(chosen_cards)

            else: # error checking
                print("Please select either '1' or '2'!")


def score_calculation(cards):
    chip_score = 0
    chip_mult = 0
    ranks = {}
    suits = {}
    straight = []
    straight_count = 0
    straight_check = False
    royal_check = False
    full_house_check = False
    flush_check = False

    cards.sort(key=lambda x: (x[3]))
    print(cards) # DEBUG

    for i in range(len(cards)): # sorts the deck's ranks out
        if cards[i][3] in ranks:
            ranks[cards[i][3]] += 1
        else:
            ranks[cards[i][3]] = 1
    ranks = dict(sorted(ranks.items(), key=lambda i: i[1]))
    print(ranks) # DEBUG

    for i in range(len(cards)): # sort the hand's suits out
        if cards[i][0] in suits:
            suits[cards[i][0]] += 1
        else:
            suits[cards[i][0]] = 1
    suits = dict(sorted(suits.items(), key=lambda i: i[1]))
    print(suits) # DEBUG

    # checks for straights - sorts the keys (using sort removes duplicates), and then checks to see if its consecutive
    # if it fails, turn to 1 and continue (take into account hands that are above 5), and if it hits 5, say straight is true
    # NEED TO UPDATE FOR HIGH AND LOW ACES!! SO FAR CAN DO HIGH!!!
    straight = sorted(ranks.keys())
    print(straight) # DEBUG
    if 14 in straight: # adds in a value of 1 if there is a straight so both high and low ace exists in the list.
        straight.append(1)
        straight.sort()
    print(straight)  # DEBUG
    for i in range(1, len(straight)):
        if straight[i] == straight[i - 1] + 1:
            straight_count += 1
            print(straight_count) # DEBUG
            if straight_count >= 4:
                straight_check = True
                straight_count = 0
                break  # stops loop once straight is found
        else:
            straight_count = 0

    if max(suits.values()) >= 5:
        flush_check = True

    # checks for royalty - just use for royal flush
    if 14 in straight and 13 in straight and 12 in straight and 11 in straight and 10 in straight:
        royal_check = True

    # checks for full house - used separately due to the weird clatter of arguements which will be neater to put under a check here.
    if 3 in ranks.values() and (2 in ranks.values() or list(ranks.values()).count(3) >= 2):
        full_house_check = True

    if max(suits.values()) == 5 and max(ranks.values()) == 5:  # FLUSH FIVE - Five cards of the same rank and suit // ADD CHIP SCORING
        chip_score += POKER_HANDS["Flush Five"][0]
        chip_mult += POKER_HANDS["Flush Five"][1]

        print("Flush Five")

    elif full_house_check == True and flush_check == True: # FLUSH HOUSE - Full House + Flush // ADD CHIP SCORING
        chip_score += POKER_HANDS["Flush House"][0]
        chip_mult += POKER_HANDS["Flush House"][1]

        print("Flush House")

    elif max(ranks.values()) == 5: # FIVE OF A KIND // ADD CHIP SCORING
        chip_score += POKER_HANDS["Five of a Kind"][0]
        chip_mult += POKER_HANDS["Five of a Kind"][1]

        print("Five of a Kind")

    elif max(suits.values()) == 5 and straight_check == True and royal_check == True: # ROYAL FLUSH - Flush by A K Q J 10 // straight check is unneeded but just in case...
        chip_score += POKER_HANDS["Royal Flush"][0]
        chip_mult += POKER_HANDS["Royal Flush"][1]

        for i in range(5):
            chip_score += cards[i][2]

        print("Royal Flush!")
        for i in range(5):
            print("Scored", cards[i][1], "of", cards[i][0])

    elif straight_check == True and max(suits.values()) == 5:  # STRAIGHT FLUSH - Straight + Flush
        chip_score += POKER_HANDS["Straight Flush"][0]
        chip_mult += POKER_HANDS["Straight Flush"][1]

        for i in range(5):
            chip_score += cards[i][2]

        print("Straight Flush!")
        for i in range(5):
            print("Scored",cards[i][1],"of",cards[i][0])

    elif max(ranks.values()) == 4:  # FOUR OF A KIND // ADD CHIP SCORING
        chip_score += POKER_HANDS["Four of a Kind"][0]
        chip_mult += POKER_HANDS["Four of a Kind"][1]

        print("Four of a Kind!")

    elif full_house_check == True: # FULL HOUSE - Three of a kind + Two of a kind // ADD CHIP SCORING
        chip_score += POKER_HANDS["Full House"][0]
        chip_mult += POKER_HANDS["Full House"][1]

        print("Full House")

    elif max(suits.values()) == 5:  # FLUSH - All cards have 1 suit
        chip_score += POKER_HANDS["Flush"][0]
        chip_mult += POKER_HANDS["Flush"][1]

        for i in range(5):
            chip_score += cards[i][2]

        print("Flush!")
        for i in range(5):
            print("Scored",cards[i][0],"of",cards[i][1])

    elif straight_check == True:  # STRAIGHT - All cards are consecutive. Order - A K Q J 10... 3 2 A
        chip_score += POKER_HANDS["Straight"][0]
        chip_mult += POKER_HANDS["Straight"][1]

        for i in range(5):
            chip_score += cards[i][2]

        print("Straight!")
        for i in range(5):
            print("Scored",cards[i][0],"of",cards[i][1])

    elif max(ranks.values()) == 3:  # THREE OF A KIND // ADD CHIP SCORING
        chip_score += POKER_HANDS["Three of a Kind"][0]
        chip_mult += POKER_HANDS["Three of a Kind"][1]

        print("Three of a Kind!")

    elif list(ranks.values()).count(2) >= 2: # TWO PAIR // ADD CHIP SCORING
        chip_score += POKER_HANDS["Two Pair"][0]
        chip_mult += POKER_HANDS["Two Pair"][1]

        print("Two Pair!")

    elif max(ranks.values()) == 2:  # PAIR // ADD CHIP SCORING
        chip_score += POKER_HANDS["Pair"][0]
        chip_mult += POKER_HANDS["Pair"][1]

        print("Pair!")

    elif max(ranks.values()) == 1:  # HIGH CARD // ADD CHIP SCORING
        chip_score += POKER_HANDS["High Card"][0]
        chip_mult += POKER_HANDS["High Card"][1]

        print("High Card!")

    return chip_score, chip_mult # // AT ENDDD! //

# ------------------------------- main module -------------------------------
print("Welcome to Balatro!")
print("Generating blind...")
print()
time.sleep(1)
blind_maker()
time.sleep(1)
new_deck()
hand_deal(HAND_SIZE)
time.sleep(1)
gameplay()