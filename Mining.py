from py_stealth import *
from datetime import *
import timeit

def bank():
    starttime = datetime.now()
    while (InJournalBetweenTimes("stones in your Bank Box", starttime, datetime.now())) < 1:
        NewMoveXY(2498, 560, True, 1, True)  # Bank
        UOSay("Bank")
        CheckLag(10000)


def TypeQuantity(type, color, container):
    if FindTypeEx(type, color, container, True):
        return FindFullQuantity()
    return 0


def ressurect():
    NewMoveXY(2552, 488, True, 1, True)  # Ank
    UseFromGround(0x0005, 0xFFFF)


def smelt():
    while FindTypesArrayEx([0x19B9, 0x19BA, 0x19B7, 0x19B8], [0xFFFF], [Backpack()], False):
        NewMoveXY(2467, 558, True, 1, True)  # Forge
        UseObject(FindItem())
        Wait(500)


def unload():
    while FindTypesArrayEx([0x1BEF, 0x1EBC], [0xFFFF], [Backpack()], False):
        MoveItem(FindItem(), 65000, ObjAtLayer(BankLayer()), 0, 0, 0)
        Wait(500)


def make_tool():
    while Count(0x0E85) < 2:
        while Count(0x1EBC) < 1:  # grab tinker tool
            if FindType(0x1EBC, ObjAtLayer(BankLayer())):
                MoveItem(FindItem(), 1, Backpack(), 0, 0, 0)
                Wait(500)
            else:
                return

        while TypeQuantity(0x1BEF, 0x0000, Backpack()) < 4:  # grab iron ingots
            if FindTypeEx(0x1BEF, 0x0000, ObjAtLayer(BankLayer()), False):
                MoveItem(FindItem(), 20, Backpack(), 0, 0, 0)
                Wait(500)
            else:
                return

        starttime = datetime.now()
        UseType2(0x1EBC)
        AutoMenu('Tinkering', 'Tools')
        AutoMenu('Tools', 'Pickaxe')
        AutoMenu('Mining Pickaxes', 'Iron pickaxe')
        WaitJournalLine(starttime, "You put|failed", 5000)

    unload()


def gettiles(radius):
    minable = range(1339,1359)
    found = []
    tempx, tempy = GetX(Self()), GetY(Self())
    for ix in range(tempx - radius, tempx + radius):
        for iy in range(tempy - radius, tempy + radius):
            tile = ReadStaticsXY(ix, iy, WorldNum())
            if tile:
                if tile[0]['Tile'] in minable:
                    found.append((tile[0]['Tile'], tile[0]['X'], tile[0]['Y'], tile[0]['Z']))
    AddToSystemJournal(found)
    return found



def mine(list):
    message_end = "Can't|" \
                  "Try mining elsewhere|" \
                  "There is nothing|" \
                  "so close|" \
                  "That is too far away|" \
                  "is attacking you|" \
                  "pickaxe is destroyed|" \
                  "fatigued|" \
                  "line of sight"
    message_attack = "is attacking you"

    for tile, x, y, z in list:
        NewMoveXY(x, y, True, 2, True)
        if Count(0x0E85) > 0:
            UseType2(0x0E85)
            starttime = datetime.now()
            WaitTargetTile(tile, x, y, z)
            WaitJournalLine(starttime, message_end, 120000)
            if ((InJournalBetweenTimes(message_attack, starttime, datetime.now())) > 0):
                UOSay("Guards")
                Wait(500)
                UOSay("Guards")
                Wait(500)

        elif Dead():
            ressurect()
            bank()
            make_tool()

        else:
            smelt()
            bank()
            unload()
            make_tool()

        if Weight() > MaxWeight() - 100:
            smelt()
            bank()
            make_tool()
            unload()


def SortTrees(trees):
    """ @param trees List of tuples(tile,x,y,z) """
    trees_by_distance = {}
    ordered_trees_list = []
    prev_last_tree = (0, start_cordinates[0], start_cordinates[1])

    def TreeDist(tree1, tree2):
        return Dist(tree1[1], tree1[2], tree2[1], tree2[2])

    for tree in trees:
        td = TreeDist(tree, prev_last_tree)
        if td % 2 == 0:
            td -= 1
        trees_group = trees_by_distance.get(td, [])
        trees_group.append(tree)
        trees_by_distance[td] = trees_group

    for current_distance in trees_by_distance:
        trees = trees_by_distance[current_distance]
        first_tree = last_tree = trees[0]
        for tree1 in trees:
            for tree2 in trees:
                if (TreeDist(tree1, tree2) > TreeDist(first_tree, last_tree)):
                    first_tree, last_tree = tree1, tree2
        if (TreeDist(prev_last_tree, last_tree) < TreeDist(prev_last_tree, first_tree)):
            first_tree, last_tree = last_tree, first_tree
        trees.sort(key=lambda tree: TreeDist(tree, first_tree))
        ordered_trees_list += trees
        prev_last_tree = last_tree

    return ordered_trees_list



if __name__ == '__main__':
    start_cordinates = (GetX(Self()), GetX(Self()))
    while (True):
        start = timeit.timeit()
        mine(SortTrees(gettiles(20)))  # Get tiles list dynamicly
        end = timeit.timeit()
        print(f"It took to mine all area {end - start}")
