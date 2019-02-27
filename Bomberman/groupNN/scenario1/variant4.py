# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from finitestatecharacterfinal import FiniteStateCharacter

wins = 0
# Create the game
<<<<<<< HEAD
for i in range(25):
    random.seed(i) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("monster", # name
                                        "A",       # avatar
                                        3, 13,     # position
                                        2          # detection range
    ))
=======
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
))
>>>>>>> 5ebee29e9459c567c9d43aec5e752f5f07f4254b

    # TODO Add your character
    g.add_character(FiniteStateCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
    ))

    # Run!
    try:
        g.go(1)
    except ValueError:
        wins+=1

print("These are the wins: " , wins)