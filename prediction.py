import numpy as np
from numpy.random import random, randint

BOARD_SIZE = 5
SHIP = 0
MISS = 1
HIT = 2
SHIPS_SIZE = [5, 4, 3, 2]
SHIPS = {'carrier': 5, 'battleship': 4, 'destroyer': 3, 'submarine': 2}
HITS_SKEW_PROBS = True
BOARD_STATE = [[-1 for x in range(5)] for x in range(5)]
boardProbabilities = [[0 for x in range(5)] for x in range(5)]
SKEW = 2


def isValidPosition(x, y, ship_size, vertical, obstacles):
    if ship_size not in SHIPS_SIZE:
        return True
    if not vertical and y + ship_size > BOARD_SIZE:
        return True
    if vertical and x + ship_size > BOARD_SIZE:
        return True

    for j in range(ship_size):
        index = getNextCell(x, y, j, vertical)
        if index in obstacles:
            return True


def getNextCell(x, y, offset, vertical):
    if vertical:
        x += offset
    else:
        y += offset
    return [x,y] #(y * 5) + x


def getSurroundingPos(pos):
    x = pos[0]
    y = pos[1]
    adj = []

    if y + 1 < BOARD_SIZE:
        adj.append([x, y + 1])
    if y - 1 >= 0:
        adj.append([x, y - 1])
    if x + 1 < BOARD_SIZE:
        adj.append([x + 1, y])
    if x - 1 >= 0:
        adj.append([x - 1, y])

    return adj


def updateProbs(pos, shipSize, vertical, bProbs):
    x = pos[0]
    y = pos[1]
    if vertical:
        z = y
    else:
        z = x
    end = z + shipSize - 1

    for i in range(z, end+1):
        if vertical:
            bProbs[x][i] = bProbs[x][i] + 1
        else:
            bProbs[i][y] = bProbs[i][y] + 1

    return bProbs


def canPlaceShip(positionMISSed, pos, shipSize, vertical, bState):
    x = pos[0]
    y = pos[1]
    if vertical:
        z = y
    else:
        z = x
    end = z + shipSize - 1

    if end > BOARD_SIZE - 1:
        return False

    for i in range(z, end+1):
        if vertical:
            thisPos = bState[x][i]
        else:
            thisPos = bState[i][y]

        if thisPos == positionMISSed:
            return False

    return True


def isPositionUnPlayed(bState, x, y):
    # if -1 then not played.
    if bState[x][y] == -1:
        return True
    else:
        return False


def getAttackPos3(bState, bProbs):
    bestProb = 0
    bestPos = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if isPositionUnPlayed(bState, x, y) and bProbs[x][y] > bestProb:
                bestProb = bProbs[x][y]
                bestPos = [x, y]

    mat = np.array(bState)
    max_value = np.max(mat)
    if max_value == -1:
        value = randint(0, 5)
        if value == 1:
            bestPos = [2, 0]
        elif value == 2:
            bestPos = [4, 2]
        elif value == 3:
            bestPos = [0, 2]
        elif value == 4:
            bestPos = [2, 4]
        else:
            bestPos = [x, y]

    return bestPos


def getAttackPos2(bState, bProbs):
    bestProb = 0
    bestPos = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if isPositionUnPlayed(bState, x, y) and bProbs[x][y] > bestProb:
                bestProb = bProbs[x][y]
                bestPos = [x, y]

    mat = np.array(bState)
    max_value = np.max(mat)
    if max_value == -1:
        value = randint(0, 5)
        if value == 1:
            bestPos = [2, 0]
        elif value == 2:
            bestPos = [4, 2]
        elif value == 3:
            bestPos = [0, 2]
        elif value == 4:
            bestPos = [2, 4]
        else:
            bestPos = [x, y]

    return bestPos

def getAttackPos1(bState, bProbs):
    bestProb = 0
    bestPos = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if isPositionUnPlayed(bState, x, y) and bProbs[x][y] > bestProb:
                bestProb = bProbs[x][y]
                bestPos = [x, y]

    mat = np.array(bState)
    return bestPos


def skewProbabilityAroundHits(toSkew, probs):
    uniques = []
    for i in range(len(toSkew)):
        toSkew += getSurroundingPos(toSkew[i])

    for i in range(len(toSkew)):
        uniques.append(' '.join([str(c) for c in toSkew[i]]))

    unique_numbers = list(set(uniques))
    for i in range(len(unique_numbers)):
        toSkew_p = unique_numbers[i].split(' ')
        toSkew_p = [int(k1) for k1 in toSkew_p]
        x = toSkew_p[0]
        y = toSkew_p[1]
        probs[x][y] *= SKEW

    return probs


def getProbs2(bState, ship_locs):
    bProbs = [[0 for x in range(5)] for x in range(5)]
    remaining_ships_list = get_unsunkShips(ship_locs)
    sunk_cells = get_sunkCells(ship_locs)
    obstacle_cells = get_obstacles(bState, sunk_cells)
    hit_cells = get_hitCells(bState, sunk_cells)

    for i in range(0, len(remaining_ships_list)):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                for direction in [True, False]:
                    ship_size = SHIPS[remaining_ships_list[i]]
                    if not isValidPosition(x, y, ship_size, direction, obstacle_cells):
                        hit_seen = 0
                        for j in range(ship_size):
                            pos = getNextCell(x, y, j, direction)
                            bProbs[pos[0]][pos[1]] += 1
                            if pos in hit_cells:
                                hit_seen += 1

                        if hit_seen:
                            for j in range(ship_size):
                                pos = getNextCell(x, y, j, direction)
                                bProbs[pos[0]][pos[1]] += 5 * hit_seen

    for p in hit_cells:
        bProbs[p[0]][p[1]] = 0

    return bProbs


def getProbs1(bState):
    hits = []
    bProbs = [[0 for x in range(5)] for x in range(5)]
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if HITS_SKEW_PROBS and bState[x][y] == HIT:
                hits.append([x, y])

    for i in range(0, len(SHIPS_SIZE)):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                #H
                if canPlaceShip(MISS, [x, y], SHIPS_SIZE[i], False, bState):
                    bProbs = updateProbs([x, y], SHIPS_SIZE[i], False, bProbs)
                #V
                if canPlaceShip(MISS, [x, y], SHIPS_SIZE[i], True, bState):
                    bProbs = updateProbs([x, y], SHIPS_SIZE[i], True, bProbs)

    if HITS_SKEW_PROBS:
        bProbs = skewProbabilityAroundHits(hits, bProbs)

    return bProbs

def get_obstacles(bState, sunk_cells):
    cells = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if [x,y] in sunk_cells or bState[x][y] == MISS:
                cells.append([x,y])
    return cells

def get_hitCells(bState, sunk_cells):
    cells = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if [x,y] not in sunk_cells and bState[x][y] == HIT:
                cells.append([x,y])
    return cells

def get_sunkCells(ship_loc):
    cells = []
    for key in ship_loc:
        for v in ship_loc[key]:
            cells.append(v)
    return cells

def get_unsunkShips(ship_loc):
    unsunk_ships = []
    if ship_loc:
        for key in ship_loc:
            for x in SHIPS.keys():
                if x != key:
                    unsunk_ships.append(x)
    else:
        unsunk_ships = list(SHIPS.keys())
    return unsunk_ships

def swapxy(l):
    fl = []
    for x in l:
        fl.append([x[1], x[0]])
    return fl

def get_sunkShips(bShips):
    ship_loc = {}
    for x in bShips:
        stype = ''
        loc = []
        for key in x:
            if key == "type":
                stype = x[key]
            if key == "cells":
                loc = swapxy(x[key])
        ship_loc[stype.lower()] = loc
    return ship_loc

#doesn't use ship locations
def predict1(data):
    #print(bState)
    bState = data['board_state']
    mat = np.array(bState)
    mat = mat.transpose()
    bState = mat.tolist()
    print(bState)
    newProbs = getProbs1(bState)
    pos = getAttackPos1(bState, newProbs)
    x = pos[0]
    y = pos[1]
    res = {"x": y, "y": x, "prob": newProbs}
    print(res)
    return res

#uses ship locations
#attacks center
def predict2(data):
    #print(bState)
    bState = data['board_state']
    bShips = data['ship_types']
    ship_loc = get_sunkShips(bShips)
    mat = np.array(bState)
    mat = mat.transpose()
    bState = mat.tolist()
    print(bState)
    newProbs = getProbs2(bState, ship_loc)
    pos = getAttackPos1(bState, newProbs)
    x = pos[0]
    y = pos[1]
    res = {"x": y, "y": x, "prob": newProbs}
    print(res)
    return res


#uses ship locations
#attacks center + random
def predict3(data):
    #print(bState)
    bState = data['board_state']
    bShips = data['ship_types']
    ship_loc = get_sunkShips(bShips)
    mat = np.array(bState)
    mat = mat.transpose()
    bState = mat.tolist()
    print(bState)
    newProbs = getProbs2(bState, ship_loc)
    pos = getAttackPos2(bState, newProbs)
    x = pos[0]
    y = pos[1]
    res = {"x": y, "y": x, "prob": newProbs}
    print(res)
    return res


def predict(data):
    #print(bState)
    bState = data['board_state']
    bShips = data['ship_types']
    ship_loc = get_sunkShips(bShips)
    mat = np.array(bState)
    mat = mat.transpose()
    bState = mat.tolist()
    print(bState)
    newProbs = getProbs2(bState, ship_loc)
    pos = getAttackPos3(bState, newProbs)
    x = pos[0]
    y = pos[1]
    res = {"x": y, "y": x, "prob": newProbs}
    print(res)
    return res


if __name__ == "__main__":
    BOARD_STATE[2][2] = MISS
    data1 = {
        'board_state': BOARD_STATE
    }
    data = {'board_state': [[-1, 1, -1, -1, -1], [1, 2, -1, -1, -1], [-1, 2, 1, -1, -1], [-1, -1, -1, 1, -1],
                     [-1, -1, -1, -1, -1]], 'ship_types': [{'type': 'Destroyer', 'cells': [[1, 1], [2, 1]]}]}
    #take from pod logs
    data = {'board_state': [[-1, -1, 1, 2, -1], [-1, 1, -1, 2, 2], [-1, -1, 1, 2, -1], [-1, -1, 1, 2, 2], [-1, -1, -1, 2, -1]],
            'ship_types': [{'type': 'Carrier', 'cells': [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3]]}]}
    data = {'board_state': [[-1, -1, 1, 2, -1], [-1, 1, -1, 2, 2], [-1, -1, 1, 2, 2], [-1, -1, 1, 2, 2], [-1, -1, -1, 2, -1]],
            'ship_types': [{'type': 'Carrier', 'cells': [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3]]}]}
    ##
    data = {'board_state': [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1]], 'ship_types': []}
    res = predict(data)
    print(res)
    print("done")