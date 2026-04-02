# balatro
# roguelike game where you score hands to beat blinds, and grab jokers to upgrade your hands against stronger blinds.
# 2.7 dts assessment
# daksh shah
# 10/3/26

# last updated - 29/3/26

# // !! PROGRAMMER'S NOTES !! //
# - For the best experience, please use MS Gothic or Snap ITC as your font. This is just for the card printing, as these fonts keep it even. (MS Gothic is my reccomendation)
# - Some conventions may stray off the original balatro game.

# modules
import random
import time

# variables
card_deck = []
hand = []
joker_deck = []
card_deck_print = ["","","",""]

card_number = 0

anti = 1
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
    "Full House" : [40,4],
    "Four of a Kind" : [60,7],
    "Straight Flush" : [100,8],
    "Royal Flush" : [100,8],
    "Five of a Kind" : [120,12],
    "Flush House" : [140,14],
    "Flush Five" : [160,16]
} # multipliers for each hand - stored by chip addition, then chip multiplier
JOKERS = [
    ["Common",[
        ["Joker","+4 Mult"],
        ["Gluttonous Joker","Played cards with Club suit give +3 Mult when scored"],
        ["Greedy Joker","Played cards with Diamond suit give +3 Mult when scored"],
        ["Lusty Joker","Played cards with Heart suit give +3 Mult when scored"],
        ["Wrathful Joker","Played cards with Spade suit give +3 Mult when scored"],
        ["Scary Face","Played face cards give +30 Chips when scored"],
        ["Jolly Joker","+8 Mult if played hand contains a Pair"],
        ["Zany Joker", "+12 Mult if played hand contains a Three of a Kind"],
        ["Mad Joker", "+10 Mult if played hand contains a Two Pair"],
        ["Crazy Joker", "+12 Mult if played hand contains a Straight"],
        ["Drool Joker", "+10 Mult if played hand contains a Flush"],
        ["Sly Joker","+50 Chips if played hand contains a Pair"],
        ["Wily Joker", "+100 Chips if played hand contains a Three of a Kind"],
        ["Clever Joker", "+80 Chips if played hand contains a Two Pair"],
        ["Devious Joker", "+100 Chips if played hand contains a Straight"],
        ["Crafty Joker", "+80 Chips if played hand contains a Flush"],
        ["Half Joker","+20 Mult if played hand contains 3 or fewer cards"],
        ["Misprint","+ 0-23 Mult"],
        ["Even Steven","Played cards with even rank give +4 Mult when scored"],
        ["Odd Todd","Played cards with odd rank give +31 Chips when scored"],
        ["Scholar","Played Aces give +20 Chips and +4 Mult when scored"],
        ["Juggler","+1 Hand Size"],
        ["Drunkard","+1 Discard"]
             ]
    ],
    ["Uncommon",[
        ["Four Fingers","All Flushes and Straights can be made with 4 card"],
        ["Fibonacci","Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored"],
        ["Dusk","Retrigger all played cards in final hand of the round"],
        ["Hack","Retrigger each played 2, 3, 4, or 5"],
        ["Burglar","When Blind is selected, gain +3 Hands and lose all discards"],
        ["Sock and Buskin","Retrigger all played face cards"],
        ["Bloodstone","1 in 2 chance for played cards with Heart suit icon Heart suit to give X1.5 Mult when scored"],
        ["Arrowhead","Played cards with Spade suit icon Spade suit give +50 Chips when scored"],
        ["Onyx Gate","Played cards with Club suit icon Club suit give +7 Mult when scored"]
                ]
    ],
    ["Rare",[
        ["Wee Joker","This Joker gains +8 Chips when each played 2 is scored"],
        ["The Duo","X2 Mult if played hand contains a Pair"],
        ["The Trio", "X3 Mult if played hand contains a Three of a Kind"],
        ["The Family", "X4 Mult if played hand contains a Four of a Kind"],
        ["The Order", "X3 Mult if played hand contains a Straight"],
        ["The Tribe", "X2 Mult if played hand contains a Flush"],
            ]
    ]
]
JOKER_RARITIES = {
    "Common" : 60,
    "Uncommong" : 30,
    "Rare" : 10,
}
JOKER_DRAW = 4
BLIND_BASE_CHIPS = [300, 800, 2000, 5000, 11000, 20000, 35000, 50000] # scores for each anti, base chips increase per anti
BLIND_MULTIPLIERS = [[1,"Small",3],[1.5,"Big",4],[2,"Boss",5]] # multiplier based on boss
BLIND_DIALOGUE = [
    [   # small blinds
        """“another one thrown down here…”\n“you still smell like the stage.”""",
        """“wait… i know you.”\n“you were funny once.”""",
        """“don’t look so lost.”\n“they all come down here eventually.”""",
        """“fresh meat… let’s see how long your pride lasts.”""",
        """“you stumble like the last one… pathetic.”"""
    ],
    [   # medium blinds
        """“still trying?”\n“they already replaced you.”""",
        """“what was it you did again?”\n“…i forgot.”""",
        """“smile.”\n“c’mon—do the face.”""",
        """“do you even remember applause?”""",
        """“your tricks are old… boring now.”"""
    ],
    [   # boss blinds
        """“perform.”\n“that’s what you do, isn’t it?”""",
        """“that grin doesn’t belong to you.”\n“it belongs to them.”""",
        """“you don’t get to stop performing.”\n“not ever.”""",
        """“show us… or fall.”""",
        """“we’ve been waiting for a real show… don’t disappoint.”"""
    ],
    [   # defeat lines
        """“…then who are you without it?”""",
        """“…boring.”\n“next.”""",
        """“…huh, that’s all?”""",
        """“…we were hoping for more.”""",
        """“…pathetic.”\n“try again… if you can.”"""
    ],
    [
    """“ugh… so easily… thrown down…”""",
    """“no… not like this… the stage… my pride…”""",
    """“h-hah… you… you weren’t supposed to…”""",
    """“this… this isn’t fair… i was supposed to last longer…”""",
    """“cursed… jester… why… why me?!”"""
    ]
]
KING_DIALOGUE = [
    [   # intro lines
        """“ah… so the jester crawled back.”\n“you were amusing… for a time.”""",
        """“did you think I’d forget you?”\n“fools always crawl back.”""",
        """“look at you… still hoping for applause?”""",
        """“crawling through shadows… pathetic.”""",
        """“your pride smells as stale as your tricks.”"""
    ],
]
JOKER_SHOP_DIALOGUE = [
    """“over here… don’t ask why. just take what you need.”""",
    """“we were once like you… broken, discarded… but we survive.”""",
    """“pick carefully… some tools are sharper than you think.”""",
    """“don’t bother talking… just follow our lead.”""",
    """“you’re quiet… i like that. maybe you’ll last longer.”""",
    """“we tried to make them laugh once… now we make sure others live.”""",
    """“fight, learn, survive… nothing else matters down here.”""",
    """“we keep what was lost… maybe it will help you.”""",
    """“don’t look for mercy… look for advantage.”""",
    """“take what’s useful… leave the rest to rot.”"""
]
HAND_SIZE = 8
SELECT_HAND_SIZE = 5
DISCARD_PLAYS = 3
HAND_PLAYS = 4
# functions

def slow_print(text): # useful for text to slowly generate, letting the player read it well.
    for i in range(len(text)):
        print(text[i], end = '')
        time.sleep(0.01) # using variable for different slow for different use
    print()

def game_start():
    slow_print("""Astus was once the crown jewel of the royal court—rome’s finest jester, unmatched in wit, timing, and spectacle. nobles gathered not for politics, but for him. Laughter followed wherever he stepped.

But laughter fades.

As years passed, the court’s taste shifted. newer acts, louder performers, sharper tricks. Astus adapted, pushed harder, gave more of himself — until there was nothing left to give.

One night, mid-performance, the king did not laugh.

That silence spread.

Astus finished his act to a hollow room. No applause. No dismissal. Just a gesture.

He was removed.

Not executed — worse. Forgotten.

He was cast into the lower vaults beneath the palace, a shifting dungeon of failed entertainers, broken personas, and discarded identities — manifested as “blinds.”

Now, the spirit of Astus awakens once again, accompanied by solely his card tricks to make it through this broken land, and to get his vengance once and for all.""")
    time.sleep(1)
    gameplay()

def blind_maker(): # makes the current blind
    global anti
    global boss_hp
    global blind
    global KING_DIALOGUE
    global BLIND_DIALOGUE
    dialouge_choose = 0
    end = False

    blind += 1 # increases the blind each time, everytime it hits 3 resets to 1 and adds 1 to anti
    if blind > 3:
        blind = 1
        anti += 1
    if anti > 3:
        end = True

    print()
    dialouge_choose = random.randint(0,4)
    if blind == 3 and anti == 3:
        slow_print("...")
        print()
        slow_print("...")
        print()
        slow_print("...")
        print()
        slow_print("A royal presence blesses your arrival...")
        print()
        slow_print(KING_DIALOGUE[0][dialouge_choose])
    else:
        slow_print(BLIND_DIALOGUE[blind][dialouge_choose])
        slow_print("Spoke the blind~")

    boss_hp = BLIND_BASE_CHIPS[anti - 1]*BLIND_MULTIPLIERS[blind-1][0] # hp is set on the anti and blind, using the base chips and multipliers above

def card_print(suit,rank,order): # card print function, just makes things easy!
    return(["|"+suit+"¯¯| ","| "+rank+" | ","|__"+suit+"| ","  "+str(order)+"   "])

def new_deck(): # makes a new deck
    global card_deck

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

    amount = min(amount, len(card_deck)) # makes it so if you want to deal 5 but only have 4, itll deal 4!
    if len(card_deck) == 0: # for if it is 0...
        print("Deck is empty! No more cards to deal.")
    else:
        for i in hand:
            if len(i) > 6: # removes the order so it redefines it for each hand
                i.pop(6)
        print(" -- HAND --")
        for i in range(0, amount): # range for the amount of times you want a card
            card = (random.randint(1, len(card_deck))) - 1
            hand.append(card_deck[card])
            card_deck.pop(card) # removes card to avoid duplicates
        hand.sort(key=lambda x: (x[5],[0])) # sorts the stuff automatically by value of card, lowest to highest followed by alphabetical order of suits
        # lambda is a key you can use for your sort function to do stuff like this ^^
        order_state = 1 # state of ordering, can order by value first or suit first (changed later)
        card_deck_print = ["", "", "", ""]  # reset each time
        # code below is to print the hand like the cards.
        for j in range(0,len(hand)):
            hand[j].append(j+1) # used to actually refer to the cards you want to select
            card_lines = card_print(hand[j][1], hand[j][3],hand[j][6])  # suit icon + rank icon
            for k in range(len(card_deck_print)):
                card_deck_print[k] += card_lines[k] + " " # basically now, each line of the card is stored in the list to print later.
            # print AFTER building everything
    for l in card_deck_print: # now, this just prints each element of the card deck to make it horizontal as it is.
        print(l)
    print("Cards left in deck:",len(card_deck)) # DEBUG


def gameplay(): # main gameplay loop
    # local variables and loops
    global order_state
    global boss_hp
    global joker_deck
    global card_deck_print
    global DISCARD_PLAYS
    global HAND_PLAYS
    global BLIND_DIALOGUE
    global KING_DIALOGUE
    global HAND_SIZE
    selection_list = []
    chosen_cards = []
    card_removal = []
    chips = []
    valid_check = 0
    damage = 0

    game_loop = True
    choice_loop = True
    card_selection_loop = True
    play_discard_loop = True
    validity = False
    game_end = False

    new_deck()
    blind_maker()
    hand.clear()
    dialouge_choose = random.randint(0,4)

    hands = HAND_PLAYS
    if "Juggler" in joker_deck:
        hand_size = HAND_SIZE + 1
    else:
        hand_size = HAND_SIZE
    discards = DISCARD_PLAYS
    if "Drunkard" in joker_deck:
        discards += 1

    while game_loop == True: # main game loop begin
        # just stuff to define each loop back
        print()
        print("Anti", anti)
        print(BLIND_MULTIPLIERS[blind - 1][1], "Blind")
        print("Score:", boss_hp)
        print("Jokers:",joker_deck)
        order_state = 1
        hand_deal(hand_size - len(hand))
        print("Hands:",hands,"—","Discards:",discards)

        game_loop = False
        choice_loop = True
        while choice_loop == True: # choice to either resort or select to play/refresh
            card_selection_loop = True
            play_discard_loop = True
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
                card_deck_print = ["", "", "", ""]  # reset each time
                for j in range(0, len(hand)):  # prints current hand, code explained above
                    hand[j].pop(6) # pop to change the order of the card so that when sorting changes, they can still play it according to order.
                    hand[j].append(j + 1)
                    card_lines = card_print(hand[j][1], hand[j][3],hand[j][6])  # suit icon + rank icon
                    for k in range(len(card_deck_print)):
                        card_deck_print[k] += card_lines[k] + " "
                    # print AFTER building everything
                for card in card_deck_print:
                    print(card)
                time.sleep(0.5)

            elif choice == "2": # chosen to select
                selection_list.clear() # clears the lists each time to avoid duplicates in any of them
                chosen_cards.clear()
                card_removal.clear()
                choice_loop = False
                while card_selection_loop == True: # error fix loops
                    valid_check = 0
                    try:
                        print("Please enter the order number of the card you'd like to select, with spaces between each card number! e.g. '1 7 8'")
                        choose_cards = input()
                        # code below checks each individual card inputted to see if it is a valid card then adds to it
                        for i in choose_cards.split(" ",SELECT_HAND_SIZE-1): # refer to the bigg chunk of code below this!
                            if int(i) < 1 or int(i) > len(hand): # if invalid hand it doesnt pass valid check...
                                pass
                            else:
                                valid_check += 1
                        if valid_check > (len(choose_cards.split(" ",SELECT_HAND_SIZE-1))-1):
                                # what this code does is takes the input e.g. "1 2 3" and separates it into different elements in a list, each element ending at the space from " ".
                                # strip then gets rid of extra stuff (white spaces by default) to leave it as the number alone, allowing the code to convert it into an integer
                                # then, just adds it to the list fo selected cards
                            for i in choose_cards.split(" ", SELECT_HAND_SIZE - 1):
                                selection_list.append(int(i.strip())) # adds in the plain numbers to a list
                        else:
                                print("Please select a valid number, from 1 to " + str(len(hand)))
                    except ValueError: # error fixing
                        print("Please enter a max of",SELECT_HAND_SIZE,"cards, and refer to the order of the card")
                        print("E.g. if you want to pick a card that is 5th from the left, please enter in 5, followed by the other cards you'd like!")
                        selection_list.clear() # clears as even upon error, the append happens sometimes (depending on the error), so clear it to make it easy
                    # code to now place these selected cards into another list of chosen cards to play
                    # this code checks the order of the card in the hand, and compares it to the number the player chose and then looks for the right card
                    # after finding the card, it adds it to the list and moves on to look for the next card
                    #print(hand) # DEBUG
                    if len(selection_list) > SELECT_HAND_SIZE or len(selection_list) < 1: # to make sure they pick 1-howevermanythelimitisonly
                        print("Please pick up to",SELECT_HAND_SIZE,"valid cards!")
                    else:
                        for i in range(0, len(selection_list)): # this code basically searches for the card you pick!
                            finding_card_loop = True
                            while finding_card_loop == True: # while the loop goes on, it checks for when the chosen number = the number of the card, then stops
                                for j in range(0,len(hand)):
                                    find_chosen_card = hand[j][6]
                                    if find_chosen_card == selection_list[i]:
                                        chosen_cards.append(hand[j]) # used later for the scoring
                                        card_removal.append(hand[j])
                                        finding_card_loop = False
                        card_selection_loop = False
                        # this code removes selected cards from hand
                        for i in card_removal:
                            if i in hand:
                               hand.remove(i)
                while play_discard_loop == True: # error fixing
                    try:
                        print("Do you want to play them or discard them? (1 to Play, 2 to Discard)")
                        choose_choice = input()
                        if choose_choice == "1": # scoring
                            if hands > 0:
                                # just sees the score amt and then reduces the score required to beat and hands
                                hands = hands - 1
                                damage = score_calculation(chosen_cards,hands)
                                boss_hp = boss_hp - damage
                                play_discard_loop = False
                            else:
                                print("No hands remaining!")
                        if choose_choice == "2":
                            # does nothing cuz like it already removes it above
                            if discards > 0: # although it removes already, we need to see if they have discards cuz if not they have to play the hand
                                discards -= 1
                                play_discard_loop = False
                            else:
                                print("No discards remaining!")
                    except ValueError: # error fixing above and below
                        print("Please select either '1' or '2'!")
            else: # error checking
                print("Please select either '1' or '2'!")
        if hands <= 0:
            slow_print(BLIND_DIALOGUE[3][dialouge_choose])
            quit()
        elif boss_hp <= 0:
            if blind == 3 and anti == 3:
                print()
                slow_print("""“n-no… this can’t be…”
“a jester… victorious?!”

“impossible… my crown… my stage… stolen!”

“you… you dare…! this is not the end!”

“curse you… fool… cursed fool!”

“how… how did you… rise above…?!”

---

Silence falls. The king is defeated.

The doors creak open… light spills into the dungeon.

You are free… the blinds scatter into nothingness.

The dungeon trembles… the jokers watch in awe.

At last… the jester walks unbound.""")
                quit()
            else:
                print()
                slow_print(BLIND_DIALOGUE[4][dialouge_choose])
                slow_print("You successfully took down the blind!")
                shop()
        else:
            game_loop = True

def shop():
    global joker_deck
    global JOKER_DRAW
    global JOKER_SHOP_DIALOGUE
    selection_list = []
    deletion = ""
    joker_rarity = 0
    joker_generated = 0
    selection = 0
    dialouge_choose = random.randint(0, 9)

    selection_loop = True
    error_message = False
    input_loop = True

    print()
    slow_print("You continue your journey, and slowly arrive to a dungeon — similar to the one you were kept in... but bigger?")
    slow_print(JOKER_SHOP_DIALOGUE[dialouge_choose])
    slow_print("Some jokers slowly surround you...\nThey seem willing to help.")
    while len(selection_list) < JOKER_DRAW: # draws 4 random jokers from the pile that is avaliable.
        joker_rarity = random.randint(1,100)
        if joker_rarity <= 60:
            joker_generated = random.randint(0,len(JOKERS[0][1])-1)
            if JOKERS[0][1][joker_generated] not in selection_list:
                selection_list.append(JOKERS[0][1][joker_generated])
        elif joker_rarity <= 90:
            joker_generated = random.randint(0,len(JOKERS[1][1])-1)
            if JOKERS[1][1][joker_generated] not in selection_list:
                selection_list.append(JOKERS[1][1][joker_generated])
        elif joker_rarity <= 100:
            joker_generated = random.randint(0,len(JOKERS[2][1])-1)
            if JOKERS[2][1][joker_generated] not in selection_list:
                selection_list.append(JOKERS[2][1][joker_generated])

    #print(selection_list) # DEBUG
    for i in range(0, len(selection_list)): # just to add a number so the user can refer to each joker when picking
        selection_list[i] = selection_list[i][:2]
        selection_list[i].append(i + 1)
    #print(selection_list) # DEBUG

    while selection_loop == True: # error fix
        try:
            input_loop = True
            print()
            for i in range(0,len(selection_list)): # printing of jokers
                print(selection_list[i][2],selection_list[i][0])
            print()
            print("Please select a joker.")
            selection = int(input())
        except ValueError: # error fix
            input_loop = False
            print("Please select a number 1 to", str(JOKER_DRAW) + "!")
        if selection >= 1 or selection <= JOKER_DRAW: # error fix
            while input_loop == True: # error fix
                try: # error fix
                    for i in selection_list:
                        if selection == i[2]: # checks and finds the joker they selected
                            print(i[0])
                            print(i[1])
                            print("Input '1' to add this joker to your deck, and '2' to go back.")
                            choice = int(input())
                            if choice == 1: # if they want to add this joker
                                for j in selection_list: # just another check to find the selected joker and add it to the deck. deletion is for later as dupe jokers don't exist
                                    if selection == j[2]:
                                        joker_deck.append(j[0])
                                        deletion = j[0]
                                input_loop = False
                                selection_loop = False
                            elif choice == 2: # if they want to go back and look
                                selection_loop = True
                                input_loop = False
                            else:
                                print("Please select either '1' or '2'!")
                except ValueError:
                    print("Please select either '1' or '2'!")
        else:
            print("Please select a number 1 to", str(JOKER_DRAW) + "!")

    #print(joker_deck) # DEBUG
    #print(deletion) # DEBUG
    #print(JOKERS) # DEBUG

    for deletion_rarity in range(0,3): # deleting the joker they picked
        for i in range(0,len(JOKERS[deletion_rarity][1])):
            if JOKERS[deletion_rarity][1][i][0] == deletion:
                JOKERS[deletion_rarity][1].pop(i)
                #print("Deleted",deletion) # DEBUG
                #print(JOKERS[deletion_rarity][1]) # DEBUG
                break

    gameplay() # // END!! //

def score_calculation(cards,hands): # whole function to calculate the scorings!
    global joker_deck
    chip_score = 0
    chip_mult = 0
    ranks = {}
    suits = {}
    scored_cards = []
    scored_cards_suits = []
    straight = []
    straight_count = []
    straight_scored = []
    flush_suit = ""
    flush_scored = []
    house_pair_ranks = []
    retriggers = []
    of_a_kind_ranks = 0
    straight_flush_limit = 5
    straight_check = False
    royal_check = False
    full_house_check = False
    flush_check = False
    wee_joker_chips = 0
    cards.sort(key=lambda x: (x[5]))
    #print(cards) # DEBUG
    print()

    if "Four Fingers" in joker_deck:
        straight_flush_limit = 4

    for i in range(len(cards)): # sorts the deck's ranks out
        if cards[i][5] in ranks:
            ranks[cards[i][5]] += 1
        else:
            ranks[cards[i][5]] = 1
    ranks = dict(sorted(ranks.items(), key=lambda i: i[1]))
    #print(ranks) # DEBUG

    for i in range(len(cards)): # sort the hand's suits out
        if cards[i][0] in suits:
            suits[cards[i][0]] += 1
        else:
            suits[cards[i][0]] = 1
    suits = dict(sorted(suits.items(), key=lambda i: i[1]))
    #print(suits) # DEBUG

    # checks for straights - sorts the keys (using sort removes duplicates), and then checks to see if its consecutive
    # also does the scoring for all straight hands!
    # if it fails, turn to 1 and continue (take into account hands that are above 5), and if it hits 5, say straight is true
    straight = sorted(ranks.keys())
    #print(straight) # DEBUG
    if 14 in straight: # adds in a value of 1 if there is a straight so both high and low ace exists in the list.
        straight.insert(0,1)
    #print(straight)  # DEBUG
    for i in range(1, len(straight)):
        if straight[i-1] not in straight_count:
            straight_count.append(straight[i-1]) # adds that number to the straight list, makes it easy to refer to the score cards later
        if straight[i] == straight[i - 1] + 1: # to add element 1 to the list also
            straight_count.append(straight[i])
            #print(straight_count) # DEBUG
            if len(straight_count) >= straight_flush_limit: # if it hits above 5!
                straight_check = True # dont break incase of 5+ card hand
        elif straight[i] != 14:
            straight_count = [straight[i]] # if it doesnt hit straight, start new run with this
    if 1 in straight_count:
        straight_count.pop(0)
        straight_count.insert(0,14) # this is just for the score since a '1' doesnt exist in balatro, it is an ace which holds order value of 14
    for i in range(0, len(straight_count)):
        for j in range(0, len(cards)): # this is for scoring, checks what card it is then pulls out the score value for it and adds it to scored cards!
            if cards[j][5] == straight_count[i]:
                straight_scored.append(cards[j][5]) # add to straight score! this is seperated to avoid dupe glitches
    #print(straight) # DEBUG
    #print(straight_count) # DEBUG
    #print(cards) # DEBUG

    # checks for flushh
    #print(straight_flush_limit) # DEBUG
    #print(max(suits.values())) # DEBUG
    if max(suits.values()) >= straight_flush_limit:
        flush_check = True

    for i in suits:
        if suits[i] >= straight_flush_limit: # if the suit is 5+ its a flush
            flush_suit = i # set suit as it
            break
    #print(flush_suit) # DEBUG
    for i in cards: # gets each card
        if i[0] == flush_suit: # if the suit if it is the same
            flush_scored.append(i[5]) # add to flush score! this is seperated to avoid dupe glitches

    # checks for royalty - just use for royal flush
    if 14 in straight and 13 in straight and 12 in straight and 11 in straight and 10 in straight:
        royal_check = True

    # checks for full house - used separately due to the weird clatter of arguments which will be neater to put under a check here.
    if 3 in ranks.values() and (2 in ranks.values() or list(ranks.values()).count(3) >= 2):
        full_house_check = True

    for i in ranks:
        if ranks[i] == max(ranks.values()):
            of_a_kind_ranks = i
        if ranks[i] >= 2:
            house_pair_ranks.append(i)
            #print("HPR",house_pair_ranks) # DEBUG

    #print(of_a_kind_ranks) # DEBUG
    #print(house_pair_ranks) # DEBUG

    # HAND CALCULATIONS
    # this just usually adds its score, mult, and prints!
    if flush_check == True and max(ranks.values()) == 5:  # FLUSH FIVE - Five cards of the same rank and suit // NOT CURRENTLY POSSIBLE WITH BASE CARDS
        chip_score += POKER_HANDS["Flush Five"][0]
        chip_mult += POKER_HANDS["Flush Five"][1]
        print("Flush Five")

    elif full_house_check == True and flush_check == True: # FLUSH HOUSE - Full House + Flush // NOT CURRENTLY POSSIBLE WITH BASE CARDS
        chip_score += POKER_HANDS["Flush House"][0]
        chip_mult += POKER_HANDS["Flush House"][1]
        print("Flush House")

    elif max(ranks.values()) == 5: # FIVE OF A KIND // NOT CURRENTLY POSSIBLE WITH BASE CARDS
        chip_score += POKER_HANDS["Five of a Kind"][0]
        chip_mult += POKER_HANDS["Five of a Kind"][1]
        print("Five of a Kind")

        for i in cards:
            if i[5] == of_a_kind_ranks:
                time.sleep(0.3)
                scored_cards.append(i[4])
                scored_cards_suits.append(i[0])
                print("Scored", i[1], i[3])

    elif max(suits.values()) >= 5 and straight_check == True and royal_check == True: # ROYAL FLUSH - Flush by A K Q J 10 // straight check is unneeded but just in case...
        chip_score += POKER_HANDS["Royal Flush"][0]
        chip_mult += POKER_HANDS["Royal Flush"][1]
        print("Royal Flush!")

        for i in range(0,len(straight_scored)):
            for j in range(0,len(cards)):
                if straight_scored[i] == cards[j][5]:
                    time.sleep(0.3)
                    scored_cards.append(cards[j][4])
                    scored_cards_suits.append(cards[j][0])
                    print("Scored",cards[j][1],cards[j][3])

    elif straight_check == True and flush_check == True:  # STRAIGHT FLUSH - Straight + Flush
        chip_score += POKER_HANDS["Straight Flush"][0]
        chip_mult += POKER_HANDS["Straight Flush"][1]
        print("Straight Flush!")

        for i in range(0,len(straight_scored)):
            for j in range(0,len(cards)):
                if straight_scored[i] == cards[j][5]:
                    time.sleep(0.3)
                    scored_cards.append(cards[j][4])
                    scored_cards_suits.append(cards[j][0])
                    print("Scored",cards[j][1],cards[j][3])

    elif max(ranks.values()) == 4:  # FOUR OF A KIND // ADD CHIP SCORING
        chip_score += POKER_HANDS["Four of a Kind"][0]
        chip_mult += POKER_HANDS["Four of a Kind"][1]
        print("Four of a Kind!")

        for i in cards:
            if i[5] == of_a_kind_ranks:
                time.sleep(0.3)
                scored_cards.append(i[4])
                scored_cards_suits.append(i[0])
                print("Scored", i[1], i[3])

    elif full_house_check == True: # FULL HOUSE - Three of a kind + Two of a kind // ADD CHIP SCORING
        chip_score += POKER_HANDS["Full House"][0]
        chip_mult += POKER_HANDS["Full House"][1]
        print("Full House")

        for i in cards:
            for j in house_pair_ranks:
                if i[5] == j:
                    time.sleep(0.3)
                    scored_cards.append(i[4])
                    scored_cards_suits.append(i[0])
                    print("Scored", i[1], i[3])

    elif flush_check == True:  # FLUSH - All cards have 1 suit
        chip_score += POKER_HANDS["Flush"][0]
        chip_mult += POKER_HANDS["Flush"][1]
        print("Flush!")

        for i in range(0,len(flush_scored)):
            for j in range(0,len(cards)):
                if flush_scored[i] == cards[j][5]:
                    time.sleep(0.3)
                    scored_cards.append(cards[j][4])
                    scored_cards_suits.append(cards[j][0])
                    print("Scored",cards[j][1],cards[j][3])

    elif straight_check == True:  # STRAIGHT - All cards are consecutive. Order - A K Q J 10... 3 2 A
        chip_score += POKER_HANDS["Straight"][0]
        chip_mult += POKER_HANDS["Straight"][1]
        print("Straight!")

        for i in range(0,len(straight_scored)):
            for j in range(0,len(cards)):
                if straight_scored[i] == cards[j][5]:
                    time.sleep(0.3)
                    scored_cards.append(cards[j][4])
                    scored_cards_suits.append(cards[j][0])
                    print("Scored",cards[j][1],cards[j][3])

    elif max(ranks.values()) == 3:  # THREE OF A KIND // ADD CHIP SCORING
        chip_score += POKER_HANDS["Three of a Kind"][0]
        chip_mult += POKER_HANDS["Three of a Kind"][1]
        print("Three of a Kind!")

        for i in cards:
            if i[5] == of_a_kind_ranks:
                time.sleep(0.3)
                scored_cards.append(i[4])
                scored_cards_suits.append(i[0])
                print("Scored", i[1], i[3])

    elif list(ranks.values()).count(2) >= 2: # TWO PAIR // ADD CHIP SCORING
        chip_score += POKER_HANDS["Two Pair"][0]
        chip_mult += POKER_HANDS["Two Pair"][1]
        print("Two Pair!")

        for i in cards:
            for j in house_pair_ranks:
                if i[5] == j:
                    time.sleep(0.3)
                    scored_cards.append(i[4])
                    scored_cards_suits.append(i[0])
                    print("Scored", i[1], i[3])

    elif max(ranks.values()) == 2:  # PAIR // ADD CHIP SCORING
        chip_score += POKER_HANDS["Pair"][0]
        chip_mult += POKER_HANDS["Pair"][1]
        print("Pair!")

        for i in cards:
            if i[5] == of_a_kind_ranks:
                time.sleep(0.3)
                scored_cards.append(i[4])
                scored_cards_suits.append(i[0])
                print("Scored", i[1], i[3])

    elif max(ranks.values()) == 1:  # HIGH CARD // ADD CHIP SCORING
        chip_score += POKER_HANDS["High Card"][0]
        chip_mult += POKER_HANDS["High Card"][1]
        print("High Card!")

        for i in cards:
            if i[5] == of_a_kind_ranks:
                time.sleep(0.3)
                scored_cards.append(i[4])
                scored_cards_suits.append(i[0])
                print("Scored", i[1], i[3])

    #print(scored_cards) # DEBUG
    # prints the cards scored and final score

    # JOKERS THAT NEED RETRIGGERING - Put before hand calculation as they do count to the card count.
    if "Dusk" in joker_deck:
        if hands == 0:
            for i in scored_cards:
                retriggers.append(i)
                print("Proc Dusk!")
                print("Retrigger", i)
    if "Hack" in joker_deck:
        for i in scored_cards:
            if i == 2 or i == 3 or i == 4 or i == 5:
                retriggers.append(i)
                print("Proc Hack!")
                print("Retrigger",i)
    if "Sock and Buskin" in joker_deck:
        for i in scored_cards:
            if i == 10:
                retriggers.append(i)
                print("Proc Sock and Buskin!")
                print("Retrigger", i)
    for i in retriggers:
        scored_cards.append(i)
    # retrigger jokers put the cards that meet their requirements in a list before adding those scoring values to the list of scored cards. May affect suits for now***

    for i in range(0,len(scored_cards)):
        chip_score += scored_cards[i]
    #print(chip_score,"*",chip_mult)

    # OTHER JOKER CALCULATIONS -
    if "Joker" in joker_deck:
        chip_mult += 4
        print("Proc Joker!")
    # cards based on suit
    for i in scored_cards_suits:
        if i == "Clubs": # clubs
            if "Gluttonous Joker" in joker_deck:
                chip_mult += 3
                print("Proc Gluttonous!")
            if "Onyx Gate" in joker_deck:
                chip_mult += 7
                print("Proc Onyx Gate!")
        if i == "Diamonds": # diamonds
            if "Greedy Joker" in joker_deck:
                chip_mult += 3
                print("Proc Greedy!")
        if i == "Hearts": # hearts
            bloodstone_proc = random.randint(1,3) # bloodstone has 1/2 chance of proc
            if "Lusty Joker" in joker_deck:
                chip_mult += 3
                print("Proc Lusty!")
        if i == "Spades": # spades
            if "Wrathful Joker" in joker_deck:
                chip_mult += 3
                print("Proc Wrathful!")
            if "Arrowhead" in joker_deck:
                chip_score += 50
                print("Proc Arrowhead!")
    if "Scary Face" in joker_deck:
        for i in scored_cards:
            if scored_cards == 10:
                chip_score += 30
                print("Proc Scary Face!")
    # cards based off the hand type
    if max(ranks.values()) >= 2: # pair
        if "Jolly Joker" in joker_deck:
            chip_mult += 8
            print("Proc Jolly Joker!")
        if "Sly Joker" in joker_deck:
            chip_score += 50
            print("Proc Sly Joker!")
    if max(ranks.values()) >= 3: # three oak
        if "Zany Joker" in joker_deck:
            chip_mult += 12
            print("Proc Zany Joker!")
        if "Wily Joker" in joker_deck:
            chip_score += 100
            print("Proc Wily Joker!")
    if list(ranks.values()).count(2) >= 2: # 2 pair
        if "Mad Joker" in joker_deck:
            chip_mult += 10
            print("Proc Mad Joker!")
        if "Clever Joker" in joker_deck:
            chip_score += 80
            print("Proc Clever Joker!")
    if straight_check == True: # straight
        if "Crazy Joker" in joker_deck:
            chip_mult += 12
            print("Proc Crazy Joker!")
        if "Devious Joker" in joker_deck:
            chip_score += 100
            print("Proc Devious Joker!")
    if flush_check == True: # flush
        if "Drool Joker" in joker_deck:
            chip_mult += 10
            print("Proc Drool Joker!")
        if "Crafty Joker" in joker_deck:
            chip_score += 80
            print("Proc Crafty Joker!")
    if "Half Joker" in joker_deck:
        if len(scored_cards) <= 3:
            chip_mult += 20
            print("Proc Half Joker!")
    if "Misprint" in joker_deck:
        misprint_mult = random.randint(1,24)
        print("Proc Misprint! +", misprint_mult)
        chip_mult += misprint_mult
    if "Even Steven" in joker_deck:
        for i in scored_cards:
            if i % 2 == 0:
                chip_mult += 4
                print("Proc Even Steven!")
    if "Odd Todd" in joker_deck:
        for i in scored_cards:
            if i % 2 != 0:
                chip_score += 31
                print("Proc Odd Todd!")
    if "Scholar" in joker_deck:
        for i in scored_cards:
            if i == 11:
                chip_mult += 4
                chip_score += 20
                print("Proc Scholar!")
    if "Fibonacci" in joker_deck:
        for i in scored_cards:
            if i == 2 or i == 3 or i == 5 or i == 8 or i == 11:
                chip_mult += 8
                print("Proc Fibonacci!")
    if "Wee Joker" in joker_deck:
        for i in scored_cards:
            if i == 2:
                wee_joker_chips += 8
                print("Proc Wee Joker!")
                chip_score += wee_joker_chips
    # mult jokers
    if i == "Hearts":  # hearts
        bloodstone_proc = random.randint(1, 3)  # bloodstone has 1/2 chance of proc
        if "Bloodstone" in joker_deck:
            if bloodstone_proc == 1:
                chip_mult = chip_mult * 1.5
                print("Proc Bloodstone!")
    if max(ranks.values()) >= 2:  # pair
        if "The Duo" in joker_deck:
            chip_mult = chip_mult * 2
            print("Proc The Duo!")
    if max(ranks.values()) >= 3:  # three oak
        if "The Trio" in joker_deck:
            chip_mult = chip_mult * 3
            print("Proc The Trio!")
    if max(ranks.values()) >= 4:  # four oak
        if "The Family" in joker_deck:
            chip_mult = chip_mult * 4
            print("Proc The Family!")
    if straight_check == True:  # straight
        if "The Order" in joker_deck:
            chip_mult = chip_mult * 3
            print("Proc The Order!")
    if flush_check == True:  # flush
        if "The Tribe" in joker_deck:
            chip_mult = chip_mult * 2
            print("Proc The Tribe!")
    #print(scored_cards) # DEBUG
    #print(scored_cards_suits) # DEBUG
    print()
    time.sleep(0.3)
    print("Scored",chip_score*chip_mult)
    time.sleep(0.3)
    return int(chip_score*chip_mult) # // AT ENDDD! //
# ------------------------------- main module -------------------------------
game_start()
