import sys
import time
import pathfinding as greedyBFS
#############################################################################################
#expectiMax(World, Character, MonsterList, [int xf, int yf], int)-> [int xOp, int yOp]
#Given a world, ticked for any bombs, a character, a monsterlist of size 1 or 2 (as there is a max of 2 monsters)
#a positional tuple of the exit, and the max depth to reach. The depth will early exit in the case of succsess (reaching
#the exit) and failure (death)
def expectiMax(wrld, Exit, Depth):
  #________________________________________________________________________________#
    #Set up charicter placement, converting charicters to optimized charicters
    Mlist = []
    t = time.time()
    for monList in wrld.monsters.values():
        for mon in monList:
            Mlist.append(mon)
    cExt = next(iter(wrld.characters.values()))[0]


    c = OpChar(cExt.x, cExt.y)
    m1 = None
    m2 = None

    if len(Mlist)==0:
        raise Exception('Trying to use expectimax with no monster')
    else:

        rnge = 2
        if Mlist[0].avatar == 'A':
            rnge = 2
        m1 = OpMonster(Mlist[0].x, Mlist[0].y, rnge)


        if len(Mlist)>=2:

            rnge = 2
            if Mlist[1].avatar == 'A':
                rnge = 2
            m2 = OpMonster(Mlist[1].x, Mlist[1].y, rnge)


  #________________________________________________________________________________#
    #tick the world once for bombs, then generate all possible lists of movements
    #generate all worlds at begining, so it doesn't have to be constantly recreated
    wrld.character = {}
    wrldList = []
    for i in range(Depth+2):

        (newwrld, events) = wrld.next()
        wrldList.append(newwrld)


    m1List = find_actions_monster(wrldList[0], m1, c, Depth)
    # m2List = find_actions_monster(wrldList[0], m2, c, Depth)


  #________________________________________________________________________________#
    #for every action possible, make a move then choose arg max

    BestAction = [-(sys.maxsize - 1), c]


    for mon in m1List:

        BestActChar = ArgMaxPlayer(wrldList, mon, c, Exit, Depth)
        if BestActChar[0] > BestAction[0]:
            BestAction = BestActChar

        #v += expVal(wrldList, m2, char, Exit, 0, Depth)

    #extract the char's movement
    print("time:", time.time()-t)

    return [BestAction[1].x, BestAction[1].y]

#############################################################################################
def ArgMaxPlayer(wrldList, m, c, Exit, Depth):
    BestAction = [-(sys.maxsize - 1), c]

    cList = find_actions_OpObj(wrldList[0], c)

    for char in cList:
        v = 0

        v += expVal(wrldList[1:], m, char, Exit, 0, Depth)

       # v += expVal(wrldList[1:], m2, char, Exit, 0, Depth)

        if v > BestAction[0]:
            BestAction = [v, char]

    # extract the char's movement
    print("act:", BestAction[1].x, BestAction[1].y)

    return BestAction

#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def expVal(wrldList, m, c, Exit, D, DMax):

    if D == DMax or ((m is not None) and moveDist(m,c)<=2) or (m is None):
        return cost(wrldList[0], m, c, Exit, D, DMax)

    v=0

    mList = find_actions_monster(wrldList[0], m, c, DMax - D)


    for mon in mList:
        p = 1/(len(mList))
        v = v + p * maxVal(wrldList[1:], mon, c, Exit, D + 1, DMax)

    return v


#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def maxVal(wrldList, m, c, Exit, D, DMax):

    if D == DMax or ((m is not None) and moveDist(m, c) <= 2) or (m is None):
        return cost(wrldList[0], m, c, Exit, D, DMax)

    v = -(sys.maxsize - 1)

    cList = find_actions_OpObj(wrldList[0], c)

    for char in cList:
        v = max(v, expVal(wrldList[1:], m, char, Exit, D + 1, DMax))

    return v


#############################################################################################
#moveDist(OpMonster, OpChar)-> int
#returns the number of movements (disreguarding walls) needed to hit the charicter
def moveDist(m, c):
    return abs(m.x - c.x)+ abs(m.y - c.y)


#############################################################################################
#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def cost(wrld, m, c, Exit, D, DMax):

    cost = 0
    cost += - .05*max(abs(Exit[0] - c.x), abs(Exit[0] - c.y))
    # Elen = greedyBFS.getPathLen([c.x, c.y], Exit, wrld)
    # if Elen is not None:
    #     cost += -Elen*.5

  # ________________________________________________________________________________#
    #set Monster cost, trigger high value for death, and early death

    if m is not None:

        currRange = max(abs(m.x - c.x), abs(m.y - c.y))
        if (currRange <= 2 and m.rnge !=0) or currRange <= 0:
            return -100**(DMax+2-D)


        cost += - 5 ** (3+m.rnge - moveDist(m, c))  #- 1.25 ** (8 - len(find_actions_OpObj(wrld, c)))


  # ________________________________________________________________________________#
    #if at the exit w/o death, nice, choose this

    if max(abs(Exit[0] - c.x), abs(Exit[1] - c.y)) <=2:
        #print("ahhh", c.x, c.y, abs(Exit[0] - c.x), abs(Exit[0] - c.y))
        return 100*(3-max(abs(Exit[0] - c.x), abs(Exit[1] - c.y)))

    return cost


#############################################################################################
#find_actions_monster(World, OpMonster, OpChar, Int)-> List[OpMonster]
#given the world, a monster, and a charicter, returns a list of monster objects in all new positions
#if close to the charicter, the only move is towards the char
#if further than 2*depth+1, then the char is too far for any movements to afftect the charicter
def find_actions_monster(wrld, m, c, DMax):
    if m is None:
        return [None]

    #if its in range, the monster walks at the charicter
    if max(abs(m.x - c.x), abs(m.y - c.y)) <= m.rnge:
        mon = OpMonster(m.x + (c.x - m.x), m.y + (c.y - m.y), m.rnge)
        mon.xP = m.x
        mon.yP = m.y
        return [mon]

    #if too far away to kill the charicter in depth number of moves, then the monster should be ignored.
    #TODO make sure this doesn't cause problems
    elif moveDist(m,c) > DMax*2+1:
        return [None]

    elif m.rnge==1:
        w = wrld.width()
        h = wrld.height()
        dx = m.x-m.xP
        dy = m.y-m.yP
        if not (dy !=0 and dx!=0) and (not (m.x+dx >= w or m.x+dx <0 or m.y+dy >= h or m.y+dy <0)) and (not wrld.wall_at(m.x+dx,m.y+dy)):
            mon= OpMonster(m.x+dx,m.y+dy, m.rnge)
            mon.xP = m.x
            mon.yP = m.y
            return [mon]
    # otherwise it moves randomly into a new safe space
        # check 8 connected for walls and out of bounds.
    actions = find_actions_OpObj(wrld, m)
    for Mon in actions:
        Mon.rnge = m.rnge
        Mon.xP = m.x
        Mon.xY = m.y

    return actions


#############################################################################################
# find_actions_Char(World, OpObj)-> List[OpChar]
# given the world and a charicter, returns a list of Charicter objects in all new positions
def find_actions_OpObj(wrld, OpObj):
    actions = []

    width = wrld.width()
    height = wrld.height()

    # check 8 connected for walls and out of bounds.
    for i in range(3):

        i -= 1

        for j in range(3):

            j -= 1

            if not (OpObj.x + i >= width or OpObj.x + i < 0 or OpObj.y + j >= height or OpObj.y + j < 0):

                if not (wrld.wall_at(OpObj.x + i, OpObj.y + j)) and not wrld.explosion_at(OpObj.x + i, OpObj.y + j):

                    if isinstance(OpObj, OpChar):
                        actions.append(OpChar(OpObj.x + i, OpObj.y + j))
                    elif (not (i == 0 and j == 0)):
                        actions.append(OpMonster(OpObj.x + i, OpObj.y + j))

    return actions


#############################################################################################
#a version of the monster that is optimized for expectimax
#takes an x,y position and a range for attack
class OpMonster:

    def __init__(self, x, y, rnge= 0):
        self.x = x
        self.y = y
        self.xP = x
        self.yP = y
        self.rnge = rnge


#x and y position
class OpChar:

    def __init__(self, x, y):
        self.x = x
        self.y = y

#############################################################################################