import math

def calcdist(rota):
	t = len(rota)	
	dist = 0
	for j in range(t-1):
		dist += d[rota[j]][rota[j+1]]
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
	sol.append(x)
	
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
	jobs.remove(novaj)
	sol.insert(posj+1,novaj)

def constructive():
	sol = []
	jobs = []
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

#solv = open("solutions.txt","w+")
with open('att48_d.txt', 'r') as f:
    d = [[int(num) for num in line.split()] for line in f]
n = len(d)

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
