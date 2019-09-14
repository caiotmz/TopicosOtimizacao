import math, time
from random import randint, random, seed, shuffle, uniform

def SortLRC(v):
    return v[0]

def lista(LRC):
    LRC.sort(key = SortLRC)
    gmin = LRC[0][0]
    gmax = LRC[-1][0]
    ge = gmin + alpha*(gmax-gmin)
    while LRC[-1][0] > ge: 
        LRC.pop(-1)

def calcdist(rota):
    t = len(rota)
    dist = 0
    for j in range(t-1):
        dist += d[rota[j]][rota[j+1]]
    dist += d[rota[j+1]][rota[0]]
    return dist

def first_pair(sol, jobs):
    LRC = []
    gmin = math.inf
    gmax = 0
    for j in range(n):
        for i in range(j+1,n):
            LRC.append([d[j][i],j,i])
    lista(LRC)
    a = randint(0,len(LRC)-1)
    jobs.remove(LRC[a][1])
    jobs.remove(LRC[a][2])
    sol.append(LRC[a][1])
    sol.append(LRC[a][2])

def insert_job(sol,jobs):
    ls = len(sol)
    LRC = []
    gmin = math.inf
    gmax = 0
    for j in jobs:
        for i in range(ls-1):
            x = d[sol[i]][j] + d[j][sol[i+1]] - d[sol[i]][sol[i+1]]
            LRC.append([x,j,i])
        x = d[sol[ls-1]][j] + d[j][sol[0]] - d[sol[ls-1]][sol[0]]
        LRC.append([x,j,ls-1])
    lista(LRC)
    a = randint(0,len(LRC)-1)
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
        if i != n-1:
            neigh[i], neigh[i+1] = neigh[i+1], neigh[i]
        else:
            neigh[i], neigh[0] = neigh[0], neigh[i]
        x = calcdist(neigh)
        if x < min_dist:
            best_sol = neigh.copy()
            min_dist = x
            return best_sol
    return best_sol

def twoopt(sol,best):
    best_sol = []
    min_dist = best
    for i in range(n):
        for j in range(i+1,n):
            neigh = sol.copy()
            neigh = neigh[:i] + list(reversed(neigh[i:j+1])) + neigh[j+1:]
            x = calcdist(neigh)
            if x < min_dist:
                best_sol = neigh.copy()
                min_dist = x
                return best_sol
    return best_sol


#solv = open("solutions.txt","w+")
with open('distancias.txt', 'r') as f:
    d = [[int(num) for num in line.split()] for line in f]
n = len(d)
iteracoes = 50
seed(123)

for iteracoes in range(1,101):
	init = time.time()
	glob_dist = math.inf
	for i in range(iteracoes):
		alpha = 0.1
		sol = constructive()
		best = calcdist(sol)
		while True:
			newsol = localsearchswap1(sol,best)
			#newsol = twoopt(sol, best)
			if newsol == []:
		    		break
			else:
		    		sol = newsol.copy()
		    		best = calcdist(sol)
		if best < glob_dist:
			glob_best = sol
			glob_dist = best
	print(iteracoes, glob_dist, time.time() - init)	
	#print("Best : ",glob_best,glob_dist)
	#print("Tempo: %s" % (time.time() - init))
