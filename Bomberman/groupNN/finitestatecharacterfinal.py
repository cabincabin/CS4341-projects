# This is necessary to find the main code
import sys
import copy
import pathfinding as greedyBFS
import pathfinding4conn as conn4
import new_expectimax.new_expectimax_V4 as EM

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
#
# We need to:
# 1) Figure out how to widen paths
# 2) Improve bomb avoidance so that it's not hardcoded
# 3) Deal with bombs and explosions in expectiMax
# 4) Higher level algorithms



class FiniteStateCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.ticked = False
        self.oldwrld = None
        self.currwrld = None


    def do(self, wrld):

        # This method calls different algorithms to find the next position to
        # move based on the finite state the character is in.

        # Find the exit to move towards
        exit = [0, 0]

        #check every gridcell for the exit. Uses the last exit found as the "goal"
        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]

        #get current position
        meX = wrld.me(self).x
        meY = wrld.me(self).y
        print("doing", meX,meY)




        # True if there is at least 1 monster within 5 steps
        isThereMonster = self.isThereMonster(wrld, meX, meY)

        # A list of bombs if there are bombs on the board, empty otherwise
        isThereBomb = self.isThereBomb(wrld, meX, meY)

        # A list of explosions if there is at least 1 explosion within 2 steps, empty otherwise
        isThereExplosion = self.isThereExplosion(wrld, meX, meY)

        if isThereBomb and isThereMonster and isThereExplosion:
            # There at least 1 bomb, 1 monster, and 1 explosion within the danger zone
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb and isThereMonster:
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb and isThereExplosion:
            # There is both at least 1 bomb and 1 explosion within 2 steps
            self.avoidanceNoMster(wrld, exit, meX, meY, isThereBomb, isThereExplosion)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb:
            # There is at least 1 bomb within 2 steps
            self.avoidanceNoMster(wrld, exit, meX, meY, isThereBomb, isThereExplosion)
        elif isThereExplosion:
            self.avoidanceNoMster(wrld, exit, meX, meY, isThereBomb, isThereExplosion)
        else:
            # There is no danger nearby
            self.greedy(wrld, exit, meX, meY)



    def MoveDist(self, start, end):
        return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

    def isThereBomb(self, wrld, meX, meY):
        bmbs = []
        # List of bombs across the entire board
        bombs = wrld.bombs.items()

        for x,bmb in bombs:
            bmbs.append(bmb)
        return bmbs

    def isThereExplosion(self, wrld, meX, meY):
        # Returns all of the close explosions
        exps = []

        # All of the explosions
        e = wrld.explosions.items()

        # Filtering only close monsters
        for x,exp in e:
            if self.MoveDist([meX, meY], [exp.x, exp.y]) <= 1:
                exps.append(exp)

        return exps


    def isThereMonster(self, wrld, meX, meY):
            # All of the monsters
            m = wrld.monsters.items()

            # Filtering only close monsters
            for x,monstr in m:
                ms = monstr
                for ms in monstr:
                    if self.MoveDist([meX, meY], [ms.x, ms.y]) <= 3:
                        return True
                return False

    def expectimax(self, wrld, exit, meX, meY):
        print("EXPECTIMAXING!")
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = EM.expectimax(wrld, exit, 5)

        # move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])

        if goTo[0] == exit[0] and goTo[1] == exit[1]:
            raise ValueError


    def greedy(self, wrld, exit, meX, meY):
        # Returns true if the character can be moved, false if not

        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)

        if goTo[0] == exit[0] and goTo[1] == exit[1]:
            print("Threw that")
            raise ValueError

        if goTo is None:
            # TODO: Improve bomb placement and pathfinding combinations
            goTo = conn4.getNextStep([meX, meY], exit, wrld)
            if wrld.wall_at(goTo[0],goTo[1]):
                self.place_bomb()
            else:
                self.move(-meX + goTo[0], -meY + goTo[1])
        else:
            #move in direction to get to x,y found in prev step
            self.move(-meX + goTo[0], -meY + goTo[1])

    def avoidanceNoMster(self, wrld, exit, meX, meY, bmbs, exps):
        print("here too")
        # Check if there are bombs
        if bmbs and not exps and self.ticked == False:
            print("here too")
            # Advance the bomb two ticks
            try:
                m = next(iter(wrld.monsters.values()))[0]
                m.move(0,0)
                wrld.characters = {}
                (newwrld, events) = wrld.next()
                (newwrld2, events) = newwrld.next()
                wrld = newwrld2
            except StopIteration:
                wrld.characters = {}
                (newwrld, events) = wrld.next()
                (newwrld2, events) = newwrld.next()
                wrld = newwrld2
            self.ticked = True
            # See if there are explosions now
            exps = []

            # All of the explosions
            e = wrld.explosions.items()

            # Filtering only close monsters
            for x,exp in e:
                if self.MoveDist([meX, meY], [exp.x, exp.y]) <= 1:
                    exps.append(exp)
            if not exps:
                exps = None
        # Check if there are any explosions
        if bmbs and not exps and self.ticked == True:
            print("here too")
            # Advance the bomb two ticks
            try:
                m = next(iter(wrld.monsters.values()))[0]
                m.move(0,0)
                wrld.characters = {}
                (newwrld, events) = wrld.next()
                wrld = newwrld
            except StopIteration:
                wrld.characters = {}
                (newwrld, events) = wrld.next()
                wrld = newwrld
            self.ticked = False
            # See if there are explosions now
            exps = []

            # All of the explosions
            e = wrld.explosions.items()

            # Filtering only close monsters
            for x,exp in e:
                if self.MoveDist([meX, meY], [exp.x, exp.y]) <= 1:
                    exps.append(exp)
            if not exps:
                exps = None
        if exps is not None:
            # If so,
            # Figure out which explosion cell is the closest
            clstOne = 0
            clstOneDist = 5000
            for e in exps:
                dist = abs(meX - e.x) + abs(meY - e.y)
                if  dist < clstOneDist:
                    clstOne = e
                    clstOneDist = dist
            if abs(meX-clstOne.x) == 0 and abs(meY-clstOne.y) == 0:
                # Move to the closest open space
                moveTo = ()
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        # If not current position
                        if i != 0 and j != 0:
                            # If within bounds:
                            if not (meX + i >= wrld.width() or meX + i < 0 or meY + j >= wrld.height() or meY + j < 0):
                                if not wrld.explosion_at(meX + i, meY + j) and not wrld.wall_at(meX + i, meY + j):
                                        # Save the space
                                        moveTo = (i, j)
                # Move to last saved space
                self.move(moveTo[0], moveTo[1])
            elif abs(meX-clstOne.x) == 0:
                # Move 1 step in the opposite direction from the explosion cell
                self.move(0, -(1/abs(meY-clstOne.y)) * abs(meY-clstOne.y))
            elif abs(meY-clstOne.y) == 0:
                # Move 1 step in the opposite direction from the explosion cell
                self.move(-(1/abs(meX-clstOne.x)) * abs(meX-clstOne.x), 0)
            else:
                # Move 1 step in the opposite direction from the explosion cell
                self.move(-(1/abs(meX-clstOne.x)) * abs(meX-clstOne.x), -(1/abs(meY-clstOne.y)) * abs(meY-clstOne.y))
        else:
            print("here")
            # If not, continue with traditional greedy
            self.greedy(wrld, exit, meX, meY)
