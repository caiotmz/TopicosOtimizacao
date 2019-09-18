import math, time
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from random import randrange, seed

def leitura(arquivo):
	f = open(arquivo, 'r')
	for i in range(3):
		line = f.readline()
	line = f.readline()
	n = int(line.split()[1])
	for i in range(3):
		line = f.readline()
	d = []

	i = 0
	d.append([])
	while i < n:
		line = f.readline()
		for num in line.split():
			if len(d[i]) != n:
				d[i].append(int(num))
			if len(d[i]) == n:
				d.append([])
				i += 1
	return d,n

def calcdist(rota):
	t = len(rota)
	dist = 0
	for j in range(t-1):
		dist += d[rota[j]][rota[j+1]]
	dist += d[rota[j+1]][rota[0]]
	return dist

def first_pair(sol, jobs):
	for j in range(n):
		jobs.append(j)
	inc = math.inf
	for j in range(n):
		for i in range(j+1,n):
			if d[j][i] < inc:
				x = j
				y = i
				inc = d[j][i]
	jobs.remove(x)
	jobs.remove(y)
	sol.append(x)
	sol.append(y)
    
def insert_job(sol,jobs):
	ls = len(sol)
	inc = math.inf
	for j in jobs:
		for i in range(ls-1):
			x = d[sol[i]][j] + d[j][sol[i+1]] - d[sol[i]][sol[i+1]]
			if x < inc:
				novaj = j
				posj = i
				inc = x
		x = d[sol[ls-1]][j] + d[j][sol[0]] - d[sol[ls-1]][sol[0]]
		if x < inc:
			novaj = j
			posj = ls-1
			inc = x        
	jobs.remove(novaj)
	sol.insert(posj+1,novaj)

def constructive():
	sol = []
	jobs = []
	first_pair(sol, jobs)
	while jobs:
		insert_job(sol,jobs)
	best = calcdist(sol)
	return sol, best

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

def buscalocal(sol,best):
	while True:
		newsol = twoopt(sol, best)
		#newsol = localsearchswap1(sol, best)
		if newsol == []:
			break
		else:
			sol = newsol.copy()
			best = calcdist(sol)
	return sol,best

def threeopt(solp):
	perturb = []
	b = randrange(1,n-1)
	c = randrange(b+1,n)
	a = randrange(b)
		
	solp1 = list(reversed(solp[:a]))+solp[a:b]+solp[b:c]+list(reversed(solp[c:]))
	perturb.append(solp1)
	perturb.append(list(reversed(solp1)))

	solp2 = solp[:a]+solp[a:b]+list(reversed(solp[b:c]))+solp[c:]
	perturb.append(solp2)
	perturb.append(list(reversed(solp2)))

	solp3 = solp[:a]+list(reversed(solp[a:b]))+solp[b:c]+solp[c:]
	perturb.append(solp3)
	perturb.append(list(reversed(solp3)))

	solp4 = solp[:a]+list(reversed(solp[a:b]))+list(reversed(solp[b:c]))+solp[c:]
	perturb.append(solp4)
	perturb.append(list(reversed(solp4)))

	solp5 = list(reversed(solp[:a]))+list(reversed(solp[a:b]))+solp[b:c]+list(reversed(solp[c:]))
	perturb.append(solp5)
	perturb.append(list(reversed(solp5)))

	solp6 = list(reversed(solp[:a]))+solp[a:b]+list(reversed(solp[b:c]))+list(reversed(solp[c:]))
	perturb.append(solp6)
	perturb.append(list(reversed(solp6)))

	solp7 = solp[:a]+solp[b:c]+solp[a:b]+solp[c:]
	perturb.append(solp7)
	perturb.append(list(reversed(solp7)))

	return perturb


def pert3opt(sol,nivel):
	solp = sol.copy()

	for j in range(nivel):
		perturb = threeopt(solp)
		distp = math.inf
		for i in range(len(perturb)):
			dd = calcdist(perturb[i])
			if dd < distp:
				distp = dd
				solp = perturb[i].copy()

	return solp, distp

def pertdest(sol,nivel):
	solp = sol.copy()
	dest = 0.10 * nivel
	destn = math.floor(dest * n)
	jobs = []
	for j in range(destn):
		x = randrange(len(solp))
		jobs.append(solp[x])
		solp.remove(solp[x])
	while jobs:
		insert_job(solp,jobs)
	distp = calcdist(solp)
	return solp, distp		

#------------------------------------------------------------------------------------------------------------

solv = open("solutionsILS.txt","w+")
files = ['br17.atsp', 'ft53.atsp', 'ft70.atsp', 'ftv33.atsp', 'ftv35.atsp', 'ftv170.atsp', 'kro124p.atsp']
otima = [39,6905,38673,1286,1473,2755,36230]

for inst in range(len(files)):
	solv.write("Instância: "+str(files[inst])+"\n")
	print("Instância: ",files[inst])
	d, n = leitura(files[inst])
	init = time.time()
	seed(10)

	sol, best = constructive()
	solv.write("Primeira Solução: "+str(best)+"\tTempo de execução: %s" % (time.time() - init)+"\n")
	print("Primeira Solução: ",best)

	sol, best = buscalocal(sol,best)
	solv.write("Solução Busca Local: "+str(best)+"\tTempo de execução: %s" % (time.time() - init)+"\n")
	first = best
	i = 0
	ibest = 0
	nivel = 1
	while i - ibest < 100:
		i += 1
		solpert, valpert = pertdest(sol,nivel)
		#solpert, valpert = pert3opt(sol,nivel)
		solpert, valpert = buscalocal(solpert,valpert)
		if (valpert < best):
			sol = solpert.copy()
			best = valpert
			ibest = i
			nivel = 1
			solv.write("Iteração: "+str(i)+"\tSolução ILS: "+str(best)+"\n")
			print("Iteração: ",i,"\tSolução ILS: ",best)
		else:
			nivel = math.ceil((i-ibest+1)/20)

	solv.write("Tempo de execução: %s" % (time.time() - init)+"\n\n")
	print("Tempo de execução: %s" % (time.time() - init))
	print()
