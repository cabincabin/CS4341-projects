# This is necessary to find the main code
import sys
import group05.astar as astar

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class GreedyCharacter(CharacterEntity):

    def __init__(self):
        self.first = True
        self.path = None

    def do(self, wrld):

        if self.first:
            # Your code here
            exit = [0, 0]
            #get current position
            meX = wrld.me(self).x
            meY = wrld.me(self).y

            #check every gridcell for the exit. Uses the last exit found as the "goal"
            for i in range(wrld.width()):

                for j in range(wrld.height()):

                    if wrld.exit_at(i, j):
                        exit = [i, j]

            astar_obj = astar.Astar([meX, meY], exit, wrld)

            self.path = astar_obj.find_path(wrld)

        else:

            next_node = 1

            while next_node is not None:

                next_node = 

            #get the [x,y] coords of the next cell to go to
            goTo = astar.getNextStep([meX, meY], exit, wrld)

            #move in direction to get to x,y found in prev step
            self.move(-meX + goTo[0], -meY + goTo[1])

        
