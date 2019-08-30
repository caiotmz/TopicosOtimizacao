import pandas as pd
import numpy as np
import time, sys, math, random

def SortLRC(v):
	return v[0]

def calcdist(rota):
	t = len(rota)	
	dist = 0
	for j in range(t-1):
		dist += d[rota[j]][rota[j+1]]
	return dist

def first_pair(sol, jobs):
	LRC = []
	gmin = math.inf
	gmax = 0
	for j in range(n):
		for i in range(j+1,n):
			LRC.append([d[j][i],j,i])
			gmin = min(gmin,LRC[-1][0])
			gmax = max(gmax,LRC[-1][0])
	ge = gmin + alpha*(gmax-gmin)
	LRC.sort(key = SortLRC)
	while LRC[-1][0] > ge: 
		LRC.pop(-1)
	a = random.randint(0,len(LRC)-1)
	jobs.remove(LRC[a][1])
	jobs.remove(LRC[a][2])
	sol.append(LRC[a][1])
	sol.append(LRC[a][2])
	sol.append(LRC[a][1])
	
def insert_job(sol,jobs):
	ls = len(sol)
	LRC = []
	gmin = math.inf
	gmax = 0
	for j in jobs:
		for i in range(ls-1):
			x = d[sol[i]][j] + d[j][sol[i+1]] - d[sol[i]][sol[i+1]]
			LRC.append([x,j,i])
			gmin = min(gmin,LRC[-1][0])
			gmax = max(gmax,LRC[-1][0])
	ge = gmin + alpha*(gmax-gmin)
	LRC.sort(key = SortLRC)
	while LRC[-1][0] > ge: 
		LRC.pop(-1)
	a = random.randint(0,len(LRC)-1)
	jobs.remove(LRC[a][1])
	sol.insert(LRC[a][2]+1,LRC[a][1])

def constructive():
	sol = []
	jobs = []
	for j in range(n):
		jobs.append(j)
	first_pair(sol, jobs)
	while jobs:
		insert_job(sol,jobs)
	return sol

def localsearchswap1(sol,best):
	best_sol = []
	min_dist = best
	for i in range(n):
		neigh = sol.copy()
		neigh[i], neigh[i+1] = neigh[i+1], neigh[i]
		x = calcdist(neigh)
		if x < min_dist:
			best_sol = neigh.copy()
			min_dist = x
			return best_sol
	return best_sol

#------------------------------------------------------------------------------------------------------------

solv = open("solutions.txt","w+")
with open('att48_d.txt', 'r') as f:
    d = [[int(num) for num in line.split()] for line in f]
n = len(d)
alpha = 0.00

sol = constructive()
best = calcdist(sol)
print("First Solution: ",sol,best)

while True:
	newsol = localsearchswap1(sol, best)
	if newsol == []:
		break
	else:
		sol = newsol.copy()
		best = calcdist(sol)
	print("Local Search Solution: ",sol,best)
