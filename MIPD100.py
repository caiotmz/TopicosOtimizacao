import gurobipy as grb
from gurobipy import *
import math
import matplotlib.pyplot as plt
import networkx as nx

def calcdist(rota):
	t = len(rota)	
	dist = 0
	for j in range(t-1):
		dist += d[rota[j]][rota[j+1]]
	return dist

def find_next(X, j):
	for i in range(n):
		if round(X[j,i].X) == 1:
			next = i		
	return next

def ver_subtour(X,j):
	subtour = [j]
	next = find_next(X,j)
	while next != j:
		subtour.append(next)
		next = find_next(X,next)
	return subtour

def escreve_sol(X):
	solucao = []
	for j in range(n):
		verif = 0
		for i in range(len(solucao)):
			if j in solucao[i]:
				verif = 1			
		if verif == 0:
			subtour = ver_subtour(X,j)
			solucao.append(subtour)
	return solucao

def enc_menor_tour(solucao):
	solucao = escreve_sol(X)
	menor_sub = 0
	for j in range(1,len(solucao)):
		if len(solucao[j]) < len(solucao[menor_sub]):
			menor_sub = j
	return solucao[menor_sub]

def printsolution(subtour):
	sol = 0
	for j in range(len_sub):
		sol += d[subtour[j]][subtour[j+1]]
		print(subtour[j], subtour[j+1],d[subtour[j]][subtour[j+1]],sol)

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

#solv = open("solutions.txt","w+")
n = len(coord)
model = grb.Model("TSP")

d = []
for j in range(n):
	d.append([])
	for i in range(n):
		dist = math.sqrt( ((coord[j][0]-coord[i][0])**2)+((coord[j][1]-coord[i][1])**2) )
		d[j].append(dist)

#Cria Variaveis
X = {}
X = model.addVars(n,n,vtype=GRB.BINARY)
#Cria FO
distance = sum(X[j,i]*d[j][i] for j in range(n) for i in range(n))
model.setObjective(distance, GRB.MINIMIZE)
#Cria Restricoes
model.addConstrs(sum(X[j,i] for i in range(n)) == 1 for j in range(n))
model.addConstrs(sum(X[j,i] for j in range(n)) == 1 for i in range(n))
model.addConstrs(X[j,j] == 0 for j in range(n))
model.update()

contador = 1

while True:
	model.optimize()	
	subtour = enc_menor_tour(X)
	len_sub = len(subtour)
	if len_sub != n:
		model.addConstr(sum(X[j,i] for j in subtour for i in subtour) <= len_sub - 1)
		model.update()
		contador += 1
	else:
		break

subtour.append(subtour[0])

bestdist = calcdist(subtour)

print(subtour, bestdist, contador)
plotTSP(subtour, coord)



