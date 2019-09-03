import math
import matplotlib.pyplot as plt
import networkx as nx

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
		if i == 0:
			neigh[n] = neigh[0]
		if i == n-1:
			neigh[0] = neigh[n]
		x = calcdist(neigh)
		if x < min_dist:
			best_sol = neigh.copy()
			min_dist = x
			return best_sol
	return best_sol

def plotTSP(sol, points):
	del sol[-1]
	x = []; y = []
	for i in sol:
		x.append(points[i][0])
		y.append(points[i][1])
    
	plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
	a_scale = float(max(x))/float(100)

    # Draw the primary path for the TSP problem
	plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale, color ='g', length_includes_head=True)
	for i in range(0,len(x)-1):
		plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale, color = 'g', length_includes_head = True)

    #Set axis too slitghtly larger than the set of x and y
	plt.xlim(0, max(x)*1.1)
	plt.ylim(0, max(y)*1.1)
	plt.show()


#------------------------------------------------------------------------------------------------------------

with open('instancia_100', 'r') as f:
    coord = [[float(num) for num in line.split()] for line in f]

n = len(coord)
d = []
for j in range(n):
	d.append([])
	for i in range(n):
		dist = math.sqrt( ((coord[j][0]-coord[i][0])**2)+((coord[j][1]-coord[i][1])**2) )
		d[j].append(dist)

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
plotTSP(sol, coord)
