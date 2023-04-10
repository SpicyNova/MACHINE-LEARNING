import matplotlib.pyplot as plt
import numpy as np
import math as m
import random as r

def perturbString(soln, random_space):
    # pick random index from soln
    indx = r.randint(0, len(soln)-1)

    # set that index of soln to a random char from char space
    soln[indx] = r.sample(random_space, 1)[0]

    return "".join(soln) # join the list and return string
#

def calcStringDiff(goal, soln):
    goal = np.array(list(goal)) # convert goal to np array

    diffCount = 0 #counting var

    # for each char in goal...
    for indx in range(len(goal) - 1):
        #...if it does not match the char at the same index in soln...
        if goal[indx] != soln[indx]:
            #...increment diffCount
            diffCount += 1
        #
    #...fin   

    return diffCount # total count of chars in wrong places
    # higher the score the worse off, closer to zero the better
#

def probOfStringAccept(k, dE, t):
    return m.exp(-k*dE / t)
#

def matchString(goal, nEpochs):
    # letters and a space to pull from
    char_space = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"

    # initial random soln
    oldSoln = "".join(r.sample(char_space, len(goal)))

    # temp set high
    t = 100

    # for each epoch...
    for epoch in range(nEpochs):
        #...find new perturbed soln...
        newSoln = perturbString(list(oldSoln), char_space)

        #...if new soln is "better" than old soln => diff(goal, soln)...
        if calcStringDiff(goal, newSoln) < calcStringDiff(goal, oldSoln):
            # ...set oldSoln equal to newSoln
            oldSoln = newSoln
        #...else...
        else:
            # calc prob of acceptance anyway => dE = scorePerturbed - scoreOriginal
            dE = calcStringDiff(goal, newSoln) - calcStringDiff(goal, oldSoln)
            prob = int(probOfStringAccept(1, dE, t) * 100)

            # if rand int < prob...
            if r.randint(1, 100) < prob:
                # ...set oldSoln equal to newSoln
                oldSoln = newSoln
            #
        #

        print(oldSoln) # to see progression for funsies

        # decrement temp
        t *= 1 - 0.3

    #...fin

    return ''.join(oldSoln)
#

print(f'\nFinal String: {matchString("Hello TV Land", 3000)}')