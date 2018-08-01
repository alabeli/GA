# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import numpy as np
import pandas as pd

def init_pop(popSize,location):
    return [random.sample(location,len(location)) for c in range(popSize)]

def test_fitness(pop,cost):
    fs = []
    totCost = sum(sum(cost))
    for e in pop:
        tripCost = 0
        for c in range(len(e)-1):
            tripCost += cost[e[c]][e[c+1]]
        fs.append(totCost - tripCost)
    return fs

def select_elite(fs,pop):
    return pop[np.argmax(fs)]

def select_chromes(fs,pop):
    totFitness = sum(fs)
    someNum = random.randint(0,totFitness)
    temp = 0
    for i in range(len(fs)):
        temp += fs[i]
        if temp >= someNum:
            c1 = pop[i]
            break
    someNum = random.randint(0,totFitness)
    temp = 0
    for i in range(len(fs)):
        temp += fs[i]
        if temp >= someNum:
            c2 = pop[i]
            break
    return c1,c2

def create_child(chrom1,chrom2,mutProb,location):
    splt = random.randint(0,len(chrom1)-1)
    child = chrom1[:splt] + chrom2[splt:]
    while len(set(child)) < len(child):
        splt = random.randint(0,len(chrom1)-1)
        child = chrom1[:splt] + chrom2[splt:]
    for c in range(len(child)):
        if random.random() <= mutProb:
            r1,r2 = random.choices(location,k=2)
            tmp = child[r1]
            child[r1] = child[r2]
            child[r2] = tmp
    return child

def new_pop(fs,pop,mutProb,location):
    newPop = []
    l = len(pop)
    newPop.append(select_elite(fs,pop))
    while len(newPop) <l:
        c1,c2 = select_chromes(fs,pop)
        newPop.append(create_child(c1,c2,mutProb,location))
    return newPop

def test(fs):
    numChromPerFS = max(np.bincount(fs))
    return numChromPerFS/len(fs)

def sol(solPop):
    solPopSet = [list(s) for s in set(tuple(e) for e in solPop)]
    freq = []
    for ps in solPopSet:
        f = 0
        for p in solPop:
            if p == ps:
                f += 1
        freq.append(f)
    return solPopSet[np.argmax(freq)]

costVal = pd.read_excel('TSP.xlsx',index_col=0)
numLoc = len(costVal)
location = list(range(numLoc))
cost = costVal.values

popSize = 50
numGen = 300
convergenceRate = 0.9
mutProb = 0.01

fitness={}
newPop={}
score={}

newPop[0] = init_pop(popSize,location)
fitness[0] = test_fitness(newPop[0],cost)
score[0] = test(fitness[0])
i=0

while((score[i] < convergenceRate) and (i <= (numGen - 1))):
    i += 1
    newPop[i] = new_pop(fitness[i-1],newPop[i-1],mutProb,location)
    fitness[i] = test_fitness(newPop[i],cost)
    score[i] = test(fitness[i])
    print(i,score[i])
    
if i == numGen:
    maxScore = 0
    for s in score.keys():
        if score[s] > maxScore:
            maxScore = score[s]
            maxScoreInd = s
        print("CR: ",maxScore,"Sol: ",sol(newPop[maxScoreInd]))
else:
    print("CR: ",score[i],"Sol: ",sol(newPop[i]))
