import matplotlib.pyplot as plt
import numpy as np
import math as m
import random as r
import copy

def findDist(town1, town2):
    return m.dist(town1, town2) # returns distance between two towns
#

def perturbTowns(towns):
    # pick two random towns
    indx1, indx2 = r.sample(range(len(towns)), 2)

    # swap order of towns chosen
    towns[indx1], towns[indx2] = towns[indx2], towns[indx1]

    return towns
#

def probOfTownAccept(k, dE, t):
    return m.exp(-k*dE / t)
#

def bestRoute(towns, nEpochs):
    # set initial random soln
    oldSoln = list(towns.keys()) # initial soln
    r.shuffle(oldSoln) # shuffle 'em

    # temp set high
    t = 100

    # for each epoch...
    for epoch in range(nEpochs):
        # ...generate randomized new soln from old soln...
        newSoln = perturbTowns(copy.deepcopy(oldSoln)) # deep copy otherwise oldSoln changes too

        # ...calc dist...
        oldSoln_dist = sum([findDist(towns[oldSoln[i]], towns[oldSoln[i+1]]) for i in range(len(oldSoln)-1)])
        newSoln_dist = sum([findDist(towns[newSoln[i]], towns[newSoln[i+1]]) for i in range(len(newSoln)-1)])
        # loops through soln set finding dist between each pair and summing the total      

        #...if newSoln is better than oldSoln...
        if(newSoln_dist < oldSoln_dist):
            # set oldSoln to newSoln
            oldSoln = newSoln
        #...else calc probability of acceptance anyway...
        else:
            # probability
            dE = newSoln_dist - oldSoln_dist
            prob = int(probOfTownAccept(1, dE, t) * 100)

            # if randNum < prob
            if r.randint(0, 100) < prob:
                # set oldSoln to new Soln
                oldSoln = newSoln
            #
        #

        #...decrement...
        t *= 0.7

    #...fin

    return oldSoln
#

start = {'a': (0, 0)} # one array holds the start
towns = {'b': (10, 0), 
         'c': (10, -10),
         'd': (0, -10),
         'e': (-10, -10),
         'f': (-10, 0),
         'g': (-10, 10),
         'h': (0, 10),
         'i': (10, 10)} # another array holds the towns that need to be visited

# find best route
print(bestRoute(towns, 100))