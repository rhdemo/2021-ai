import numpy as np

BOARD_SIZE = 5
SHIP = 0
MISS = 1
HIT = 2
SHIPS_SIZE = [5, 4, 3, 2]
HITS_SKEW_PROBS = True
BOARD_STATE = [[-1 for x in range(5)] for x in range(5)]
boardProbabilities = [[0 for x in range(5)] for x in range(5)]
SKEW = 2

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


def getAttackPos(bState, bProbs):
    bestProb = 0
    bestPos = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if isPositionUnPlayed(bState, x, y) and bProbs[x][y] > bestProb:
                bestProb = bProbs[x][y]
                bestPos = [x, y]

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


def getProbs(bState):
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


def predict(bState):
    #print(bState)
    mat = np.array(bState)
    mat = mat.transpose()
    bState = mat.tolist()
    print(bState)
    newProbs = getProbs(bState)
    pos = getAttackPos(bState, newProbs)
    x = pos[0]
    y = pos[1]
    res = {"x": y, "y": x, "prob": newProbs}
    print(res)
    print("---")
    return res


if __name__ == "__main__":
    BOARD_STATE[2][2] = MISS
    res = predict(BOARD_STATE)
    print(res)
    print("done")