# pokemon
# store dictionaries in a matrix

import random
import time

wild_pokemon = [
    {"Name" : "Eevee",
    "Type" : "Normal",
    "Pokedex" : 133,
    "Level" : random.randint(1,3),
    "Health" : random.randint(45,55),
    "Attack" : ["Swift",6]
    },
    {"Name" : "Lopunny",
    "Type" : "Normal",
    "Pokedex" : 133,
    "Level" : random.randint(1, 3),
    "Health": random.randint(55, 65),
    "Attack" : ["Headbutt",7]
    },
    {"Name" : "Meowscarada",
    "Type" : ["Grass","Dark"],
    "Pokedex": 908,
    "Level" : random.randint(1, 3),
    "Health" : random.randint(71,81),
    "Attack" : ["Flower Trick",7]
    },
    {"Name" : "Ceruledge",
    "Type" : ["Fire","Ghost"],
    "Pokedex": 937,
    "Level" : random.randint(1, 3),
    "Health" : random.randint(70, 80),
    "Attack" : ["Bitter Blade",9]
    },
    {"Name" : "Primarina",
    "Type" : ["Water","Fairy"],
    "Pokedex": 730,
    "Level": random.randint(1, 3),
    "Health": random.randint(75, 85),
    "Attack" : ["Sparkling Aria",9]
    },
    {"Name" : "Sogaleo",
    "Type": ["Psychic","Steel"],
    "Pokedex": 791,
    "Level": random.randint(1, 3),
    "Health": random.randint(132, 142),
    "Attack" : ["Sunsteel Strike",10]
    }
]

own_pokemon = [
    {"Name": "Eevee",
     "Type": "Normal",
     "Pokedex": 133,
     "Level": random.randint(1, 3),
     "Health": random.randint(45, 55),
     "Attack" : [" G-Max Cuddle",random.randint(9,15)]
     }
]


# Functions
def overworld_timer():
    timer = random.randint(1,5)
    print(timer)
    time.sleep(timer)
    print("Battle begin!")
    battle()

def battle():
    x = random.randint(0,len(wild_pokemon)-1)
    enemy_pokemon = wild_pokemon[x]
    player_pokemon = own_pokemon[0]
    player_pokemon_hp = player_pokemon["Health"]

    print("Player pokemon:",player_pokemon["Name"])
    print("PLayer pokemon HP:",player_pokemon_hp)

    print("A wild",enemy_pokemon["Name"],"appeared!")
    print("It's a",enemy_pokemon["Type"],"type pokemon!")
    print("It is also level",enemy_pokemon["Level"],"!")
    print("It has",enemy_pokemon["Health"],"health.")
overworld_timer()
