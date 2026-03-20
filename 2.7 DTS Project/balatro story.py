# balatro
# roguelike game where you score hands to beat blinds, and grab jokers to upgrade your hands against stronger blinds.
# 2.7 dts assessment
# daksh shah
# 10/3/26

# last updated - 10/3/26

# // !! PROGRAMMER'S NOTES !! //
# - For the best experience, please use MS Gothic or Snap ITC as your font. This is just for the card printing, as these fonts keep it even. (MS Gothic is my reccomendation)

# // STORY //
# Follows the story of Astus, a Jester from Ancient Rome.

# modules
import random
import time

# variables
card_deck = []
hand = []
card_deck_print = ["","",""]

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
SUIT_ICON = ["♥","♦","♧","♤"]
## 🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂬 🂭 🂮
## 🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂼 🂽 🂾
## 🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃌 🃍 🃎
## 🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃜 🃝 🃞
CARDS = ["Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]
CARD_ICONS = ["2","3","4","5","6","7","8","9","X","J","Q","K","A"]

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
HAND_SIZE = 8
SELECT_HAND_SIZE = 5

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

def card_print(suit,rank): # card print function, just makes things easy!
    return(["|"+suit+"¯¯| ","| "+rank+" | ","|__"+suit+"| "])

def new_deck(): # makes a new deck
    card_deck.clear() # clear old deck
    for i in range(1, 10): # prints out the number cards, uses for loops to make 44 of these
        for j in range(4):
            card_deck.append([SUIT[j], SUIT_ICON[j], CARDS[i - 1], CARD_ICONS[i-1], i+1, i+1])
    for k in range(9, 13): # same as above but face cards + ace
        for j in range(4):
            if k == 12:
                card_deck.append([SUIT[j], SUIT_ICON[j], CARDS[k], CARD_ICONS[k], 11, k + 2]) # different for ace as ace has 11 points.
            else:
                card_deck.append([SUIT[j], SUIT_ICON[j], CARDS[k], CARD_ICONS[k], 10, k+2])
    #print(card_deck) # DEBUG

    # cards are lists that store values in this order - Suit, Suit Icon, Rank, Rank Icon, Card Value (for scoring), and priority order from 2 - A.


def hand_deal(amount): # deals you the hand
    global card_deck_print # to refer to print the cards.

    print(" -- HAND --")
    for i in range(0, amount): # range for the amount of times you want a card
        card = (random.randint(1, len(card_deck))) - 1
        hand.append(card_deck[card])
        card_deck.pop(card) # removes card to avoid duplicates
    hand.sort(key=lambda x: (x[5],[0])) # sorts the stuff automatically by value of card, lowest to highest followed by alphabetical order of suits
    # lambda is a key you can use for your sort function to do stuff like this ^^
    order_state = 1 # state of ordering, can order by value first or suit first (changed later)
    card_deck_print = ["", "", ""]  # reset each time
    # code below is to print the hand like the cards.
    for j in range(0,amount):
        hand[j].append(j+1) # used to actually refer to the cards you want to select
        card_lines = card_print(hand[j][1], hand[j][3])  # suit icon + rank icon
        for k in range(3):
            card_deck_print[k] += card_lines[k] + " " # basically now, each line of the card is stored in the list to print later.
        # print AFTER building everything
    for l in card_deck_print: # now, this just prints each element of the card deck to make it horizontal as it is.
        print(l)


def gameplay(): # main gameplay loop
    # local variables and loops
    global order_state
    global card_deck_print
    selection_list = []
    chosen_cards = []
    chips = []
    valid_check = 0

    game_loop = True
    choice_loop = True
    card_selection_loop = True
    validity = False

    while game_loop == True: # main game loop begin
        while choice_loop == True: # choice to either resort or select to play/refresh
            print()
            print("Enter 1 to switch sort between 'by number' and 'by suit', Enter 2 to select cards.")
            choice = input()
            if choice == "1": # sort
                if order_state == 1: # if by number, do suit
                    hand.sort(key=lambda x: (x[0], [5]))
                    order_state = 2
                elif order_state == 2: # opposite of above
                    hand.sort(key=lambda x: (x[5], [0]))
                    order_state = 1
                card_deck_print = ["", "", ""]  # reset each time
                for j in range(0, len(hand)):  # prints current hand, code explained above
                    hand[j].pop(6) # pop to change the order of the card so that when sorting changes, they can still play it according to order.
                    hand[j].append(j + 1)
                    card_lines = card_print(hand[j][1], hand[j][3])  # suit icon + rank icon
                    for k in range(3):
                        card_deck_print[k] += card_lines[k] + " "
                    # print AFTER building everything
                for card in card_deck_print:
                    print(card)


                time.sleep(1)
            elif choice == "2": # chosen to select
                choice_loop = False
                while card_selection_loop == True:
                    valid_check = 0
                    try:
                        print("Please enter the order number of the card you'd like to select, from left to right. (E.g. 1 for the 1st card, 7 for the 7th)")
                        cards_chosen = input()
                        for i in cards_chosen.split(" ",SELECT_HAND_SIZE-1):
                            if int(i) < 1 or int(i) > len(hand):
                                pass
                            else:
                                valid_check += 1
                        if valid_check > (len(cards_chosen.split(" ",SELECT_HAND_SIZE-1))-1):
                                # what this code does is takes the input e.g. "1 2 3" and separates it into different elements in a list, each element ending at the space from " ".
                                # strip then gets rid of extra stuff (white spaces by default) to leave it as the number alone, allowing the code to convert it into an integer
                                # then, just adds it to the list fo selected cards
                            for i in cards_chosen.split(" ", SELECT_HAND_SIZE - 1):
                                selection_list.append(int(i.strip()))
                        else:
                                print("Please select a valid number, from 1 to " + str(len(hand)))
                    except ValueError: # error fixing
                        print("Please enter a max of",SELECT_HAND_SIZE,"cards, and refer to the order of the card")
                        print("E.g. if you want to pick a card that is 5th from the left, please enter in 5, followed by the other cards you'd like!")
                        selection_list.clear() # clears as even upon error, the append happens sometimes (depending on the error), so clear it to make it easy

                    # code to now place these selected cards into another list of chosen cards to play
                    # this code checks the order of the card in the hand, and compares it to the number the player chose and then looks for the right card
                    # after finding the card, it adds it to the list and moves on to look for the next card
                    if len(selection_list) > SELECT_HAND_SIZE or len(selection_list) < 1: # to make sure they pick 1-howevermanythelimitisonly
                        print("Please pick up to",SELECT_HAND_SIZE,"valid cards!")
                    else:
                        for i in range(0, len(selection_list)): # this code basically searches for the card you pick!
                            finding_card_loop = True
                            while finding_card_loop == True: # while the loop goes on, it checks for when the chosen number = the number of the card, then stops
                                for j in range(0,len(hand)):
                                    find_chosen_card = hand[j][6]
                                    if find_chosen_card == selection_list[i]:
                                        chosen_cards.append(hand[j])
                                        finding_card_loop = False
                        card_selection_loop = False
                score_calculation(chosen_cards)
            else: # error checking
                print("Please select either '1' or '2'!")

def score_calculation(cards): # whole function to calculate the scorings!
    chip_score = 0
    chip_mult = 0
    ranks = {}
    suits = {}
    scored_cards = []
    straight = []
    straight_count = 0
    straight_check = False
    royal_check = False
    full_house_check = False
    flush_check = False

    cards.sort(key=lambda x: (x[5]))
    print(cards) # DEBUG

    for i in range(len(cards)): # sorts the deck's ranks out
        if cards[i][5] in ranks:
            ranks[cards[i][5]] += 1
        else:
            ranks[cards[i][5]] = 1
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
    #print(straight) # DEBUG
    if 14 in straight: # adds in a value of 1 if there is a straight so both high and low ace exists in the list.
        straight.append(1)
        straight.sort()
    #print(straight)  # DEBUG
    for i in range(1, len(straight)):
        if straight[i] == straight[i - 1] + 1:
            straight_count += 1
            #print(straight_count) # DEBUG
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

    # checks for full house - used separately due to the weird clatter of arguments which will be neater to put under a check here.
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

        print("Royal Flush!")

    elif straight_check == True and max(suits.values()) == 5:  # STRAIGHT FLUSH - Straight + Flush
        chip_score += POKER_HANDS["Straight Flush"][0]
        chip_mult += POKER_HANDS["Straight Flush"][1]

        print("Straight Flush!")

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

        print("Flush!")

    elif straight_check == True:  # STRAIGHT - All cards are consecutive. Order - A K Q J 10... 3 2 A
        chip_score += POKER_HANDS["Straight"][0]
        chip_mult += POKER_HANDS["Straight"][1]

        for i in range(5):
            chip_score += cards[i][2]

        print("Straight!")

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