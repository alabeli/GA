# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import numpy as np

def init_pop(popSize,quantity):
    return [[random.randint(0,q) for q in quantity] for c in range(popSize)]

def test_fitness(pop,cost,weight,maxWeight):
    fs = []
    w = 0
    for e in pop:
        w = sum(np.multiply(e,weight))
        if w <= maxWeight:
            fs.append(sum(np.multiply(e,cost)))
        else:
            while w > maxWeight:
                nonZeros = [i for i,v in enumerate(e) if v>0]
                r = random.choice(nonZeros)
                newQty = random.randint(0,e[r]-1)
                w += weight[r] * (newQty - e[r])
                e[r] = newQty
            fs.append(sum(np.multiply(e,cost)))
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

def create_child(chrom1,chrom2,mutProb,quantity):
    splt = random.randint(0,len(chrom1)-1)
    child = chrom1[:splt] + chrom2[splt:]
    for c in range(len(child)):
        if random.random() <= mutProb:
            child[c] = abs(quantity[c] - child[c])
    return child

def new_pop(fs,pop,mutProb,quantity):
    newPop = []
    l = len(pop)
    newPop.append(select_elite(fs,pop))
    while len(newPop) <l:
        c1,c2 = select_chromes(fs,pop)
        newPop.append(create_child(c1,c2,mutProb,quantity))
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

quantity = [1,1,1,1]
weight = [1,5,3,4]
cost = [15,10,9,5]
maxWeight = 8

# =============================================================================
# weight = [50,100,23,56,200]
# cost = [10,5,8,15,180]
# maxWeight = 350
# =============================================================================

nc = len(weight)
popSize = 30
numGen = 300
convergenceRate = 0.9
mutProb = 0.01

fitness={}
newPop={}
score={}

newPop[0] = init_pop(popSize,quantity)
fitness[0] = test_fitness(newPop[0],cost,weight,maxWeight)
score[0] = test(fitness[0])
i=0

while((score[i] < convergenceRate) and (i <= (numGen - 1))):
    i += 1
    newPop[i] = new_pop(fitness[i-1],newPop[i-1],mutProb,quantity)
    fitness[i] = test_fitness(newPop[i],cost,weight,maxWeight)
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
