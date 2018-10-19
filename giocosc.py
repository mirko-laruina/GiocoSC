from sympy.utilities.iterables import multiset_permutations
import numpy as np
import sys, os


def printd(*args):
    if(DEBUG==True):
        print(*args)

DEBUG = False
HISTORY_THRESHOLD = 1000

Ntot = 20
N4 = 14
N3 = 2
N2 = 2
N1 = 2

startingUnified = [4]*N4 + [3]*N3 + [2]*N2 + [1]*N1
startingUnified = np.array(startingUnified, np.int8)
iterations = 0
max_moves = 0
for currentSet in multiset_permutations(startingUnified):
    iterations = iterations+1
    starting0 = currentSet[:Ntot//2]
    starting1 = currentSet[Ntot//2:]
    if iterations % 10000 == 0:
        print("ITERATION:", iterations, starting0, starting1, max_moves)
        max_moves = 0

    #starting0 = [1, 3, 4, 2, 4, 2, 4, 4, 4, 4]
    #starting1 = [4, 4, 3, 4, 1, 4, 4, 4, 4, 4]

    #Start playing!
    #0 always starts first
    s0 = list(currentSet[:Ntot//2])
    s1 = list(currentSet[Ntot//2:])
    s = [s0, s1]
    buf = []
    who = 0
    moves = 0
    history = []
    found = False
    save_history = False
    tries = -1

    while found == False and not ( len(s[0]) == 0 or len(s[1]) == 0) :
        found = False
        moves = moves+1

        #printd("Move:", moves)
        #printd("Turn:", who)

        currElem = s[who].pop(0)
        buf.append(currElem)
        if currElem < 4:
            who = (who+1)%2
            tries = currElem
        #when currElem >= 4 and tries >= 0: player under attack
        elif tries >= 0:
            tries = tries - 1
            #Attack successful
            if tries == 0:
                who = (who+1)%2
                s[who].extend(buf)
                buf.clear()
                tries = -1
        #currEleme >= 4 and tries == -1: no player is being attacked
        else:
            who = (who+1)%2

        #printd("s[0]:", s[0])
        #printd("s[1]:", s[1])
        #printd("buffer:", buf)
        #printd('--------------------------------------')

        #It should be quicker ignoring saving history and do it on request
        if save_history == True:
            #Building a unique string for history
            s_history = s[0]+[-1]+s[1]+[-1]+buf+[-1]+[who]
            for item in history:
                if item == s_history:
                    print("Cycling on", starting0, starting1)
                    print("Period:", len(history)-history.index(item))
                    history.clear()
                    found = True
                    save_history = False
            history.append(s_history)

        if moves > HISTORY_THRESHOLD:
            save_history = True
            s[0] = list(starting0)
            s[1] = list(starting1)
            buf.clear()
            who = 0
            moves = 0
        
    if moves > max_moves:
        max_moves = moves
