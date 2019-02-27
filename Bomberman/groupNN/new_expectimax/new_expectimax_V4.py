import sys
import time

def expectimax(wrld, exit, depth):
    # ________________________________________________________________________________#
    # Set up charicter placement, converting charicters to optimized charicters
    Mlist = []
    t = time.time()

    # Add all the monsters to a monster list
    for monList in wrld.monsters.values():
        for mon in monList:
            Mlist.append(mon)

    # Get our character
    cExt = next(iter(wrld.characters.values()))[0]

    # Create our own version of the character
    c = OpChar(cExt.x, cExt.y)

    print("START:", c.x, c.y)
    m1 = None
    m2 = None

    if len(Mlist) == 0:
        # There are no monsters, so don't run expectimax
        raise Exception('Trying to use expectimax with no monster')
    else:

        # Add monster type
        rnge = 1
        if Mlist[0].name == 'aggressive':
            # Aggressive type so change the range
            rnge = 2
        m1 = OpMonster(Mlist[0].x, Mlist[0].y, rnge)

        if len(Mlist) >= 2:

            rnge = 1
            if Mlist[1].name == 'aggressive':
                # Aggressive type so change the range
                rnge = 2
            m2 = OpMonster(Mlist[1].x, Mlist[1].y, rnge)

    wrld_list = []

    for i in range(2 * depth + 1):
        wrld_list.append(wrld)

    c_list = find_actions_OpObj(wrld_list[0], c)

    m1_list = find_actions_monster(wrld_list[0], m1, c, depth)

    best_action = [-(sys.maxsize - 1), c]

    for char in c_list:

        v = 0

        for m in m1_list:

            v += max_node(wrld_list[1:], m, char, exit, 0 , depth)

        if (v/len(m1_list)) > best_action[0]:
            best_action = [(v/len(m1_list)), char]
    return [best_action[1].x, best_action[1].y]

def exp_node(wrld_list, m, c, exit, d, dmax):

    v = 0

    mList = find_actions_monster(wrld_list[0], m, c, dmax - d)

    # #TODO MAYBE PROBLEMS????
    # if mList[0] is None and len(mList) == 1:
    #     return max_node(wrld_list[1:], None, c, exit, d + 1, dmax)

    for mon in mList:
        p = 1/(len(mList))
        a = max_node(wrld_list[1:], mon, c, exit, d + 1, dmax)
        v = v + p * a

    return v


def max_node(wrld_list, m, c, exit, d, dmax):

    if d <= dmax or ((m is not None) and moveDist(m, c) <= 1):
        # We are dead or have reached max depth
        return cost(wrld_list[0], m, c, exit, d, dmax)

    v = (-sys.maxsize - 1)

    c_list = find_actions_OpObj(wrld_list[0], c)

    for char in c_list:
        v = max(v, exp_node(wrld_list[1:], m, char, exit, d, dmax))


#moveDist(OpMonster, OpChar)-> int
#returns the number of movements (disreguarding walls) needed to hit the charicter
def moveDist(m, c):
    return abs(m.x - c.x)+ abs(m.y - c.y)

#expVal(OpMonster, OpMonster, OpChar, [int x, int y], int currentDepth, int Maxdepth)-> int value
def cost(wrld, m, c, Exit, D, DMax):

    cost = 0
    cost += - 10 * max(abs(Exit[0] - c.x), abs(Exit[1] - c.y))

    if m is not None:

        currRange = max(abs(m.x - c.x), abs(m.y - c.y))

        if (currRange <= 1 and m.rnge !=0) or currRange <= 0:
            return -(100**((DMax-D)+1))

        # Steer away from monsters
        cost += - 5 ** (2 * (m.rnge - moveDist(m, c)))

    # Stay young and free
    cost += 1.5 * (9 - len(find_actions_OpObj(wrld, c)))

    #if at the exit w/o death, nice, choose this

    if max(abs(Exit[0] - c.x), abs(Exit[1] - c.y)) <= 2:
        return 100 ** (5 - max(abs(Exit[0] - c.x), abs(Exit[1] - c.y)))

    return cost

#if close to the charicter, the only move is towards the char
#if further than 2*depth+1, then the char is too far for any movements to afftect the charicter
def find_actions_monster(wrld, m, c, DMax):
    if m is None:
        return [None]

    # print("Spotted character: ", c.x, c.y)
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

    elif m.rnge == 2:
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

    # print("Monster: ", m.x, m.y)
    # for m in actions:
    #
    #     print("  ", m.x, m.y)
    return actions

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
                    else:
                        #if monster and total moves less than 8, can stay still if walking into wall
                        actions.append(OpMonster(OpObj.x + i, OpObj.y + j))

    return actions

# a version of the monster that is optimized for expectimax
# takes an x,y position and a range for attack
class OpMonster:

    def __init__(self, x, y, rnge=0):
        self.x = x
        self.y = y
        self.xP = x
        self.yP = y
        self.rnge = rnge

# x and y position
class OpChar:

    def __init__(self, x, y):
        self.x = x
        self.y = y
