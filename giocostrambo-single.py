from sympy.utilities.iterables import multiset_permutations
import numpy as np
import sys, os

DEBUG = False

def printd(*args):
    if(DEBUG==True):
        print(*args)

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
    #1 always starts first
    s0 = list(currentSet[:Ntot//2])
    s1 = list(currentSet[Ntot//2:])
    s = [s0, s1]
    buf = []
    who = 0
    moves = 0
    history = []
    found = False
    save_history = False

    while found == False and not ( len(s[0]) == 0 or len(s[1]) == 0) :
        found = False

        moves = moves+1
        printd("Move:", moves)

        
        printd("Turn:", who)
        buf.append(s[who][0])
        if s[who].pop(0) < 4:
            who = (who+1)%2

        """
        if who%2:
            printd("Turn:", 1)
            buf.append(s[0][0])
            if s[0].pop(0) < 4:
                who = who+1
        else:
            printd("Turn:", 2)
            buf.append(s[1][0])
            if s[1].pop(0) < 4:
                who = who+1
        """
        

        tries = -1
        printd("Current buffer", buf)
        for i in buf:
            if i >= 4 and tries > 0:
                tries = tries - 1
                if tries == 0:
                    printd("Appending buffer:", buf)
                    s[(who+1)%2].extend(buf)
                    
                    #if not who%2:
                    #    s[1].extend(buf)
                    #else:
                    #    s[0].extend(buf)
                    
                    buf = []
            elif i < 4:
                    tries = i


        if(len(buf) == 0 or tries == -1):
            who = (who+1)%2;


        printd("s[0]:", s[0])
        printd("s[1]:", s[1])
        printd("buffer:", buf)
        printd('--------------------------------------')

        #It should be quicker ignoring saving history and do it on request
        if save_history == True:
            #Building a unique string for history
            s_history = s[0]+[-1]+s[1]+[-1]+buf+[-1]+[who]
            for item in history:
                if item == s_history:
                    print("Cicle?", starting0, starting1)
                    print("Period:", len(history)-history.index(item))
                    history.clear()
                    found = True
                    save_history = False
            history.append(s_history)

        """ OLD METHOD: it doesn't work
        try:
            if ((s[0] == starting0 and s[1] == starting1) or (s[0] == starting1 and s[1] == starting0)):
                print(s[0], starting0, s[1], starting1)
                print("FOUND?")
                sys.exit(0)
        except Exception as err:
            continue

        """
        if moves > 1000:
            save_history = True
            s[0] = starting0
            s[1] = starting1
            buf.clear()
            who = 0
            moves = 0
        
    if moves > max_moves:
        max_moves = moves
