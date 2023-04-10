# %% IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import math as m
import random as r
import copy

# %% ACCEPTANCE FUNCTION
def f(k, dE, t):
    return m.exp(-k*dE / t)
#

x = np.arange(100, 0, -1) # x values 100 to 0 counting down by 1

'''when k = 1'''
fig1, (plot1, plot2) = plt.subplots(1,2, figsize = (10, 5))
fig1.suptitle('When k = 1')

plot1.plot(x, [f(1, 1, x) for x in x]) #pos dE
plot1.invert_xaxis() # makes x-axis 100>>0 instead of 0>>100
plot1.set_title('Positive dE')
plot2.plot(x, [f(1, -1, x) for x in x]) #neg dE
plot2.invert_xaxis()
plot2.set_title('Negative dE')

plt.show()

'''when k = 10'''
fig10, (plot1, plot2) = plt.subplots(1,2, figsize = (10, 5))
fig10.suptitle('When k = 10')

plot1.plot(x, [f(10, 1, x) for x in x]) #pos dE
plot1.invert_xaxis()
plot1.set_title('Positive dE')
plot2.plot(x, [f(10, -1, x) for x in x]) #neg dE
plot2.invert_xaxis()
plot2.set_title('Negative dE')

plt.show()

'''when k = 40'''
fig40, (plot1, plot2) = plt.subplots(1,2, figsize = (10, 5))
fig40.suptitle('When k = 40')

plot1.plot(x, [f(40, 1, x) for x in x]) #pos dE
plot1.invert_xaxis()
plot1.set_title('Positive dE')
plot2.plot(x, [f(40, -1, x) for x in x]) #neg dE
plot2.invert_xaxis()
plot2.set_title('Negative dE')

plt.show()

# %% STRING MATCHING
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

# %% TRAVELING SALESMAN PROBLEM
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