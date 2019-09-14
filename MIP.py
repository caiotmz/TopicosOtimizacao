import gurobipy as grb
import time
from gurobipy import *

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

def printtime(subtour):
	sol = 0
	for j in range(len_sub):
		sol += tempo[subtour[j]][subtour[j+1]]
		print(subtour[j], subtour[j+1],tempo[subtour[j]][subtour[j+1]],sol)

#------------------------------------------------------------------------------------------------------------

with open('distancias.txt', 'r') as f:
    d = [[int(num) for num in line.split()] for line in f]

#solv = open("solutions.txt","w+")
n = len(d)
model = grb.Model("TSP")

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

cont = 1
init = time.time()
while True:
	model.optimize()	
	subtour = enc_menor_tour(X)
	len_sub = len(subtour)
	if len_sub != n:
		model.addConstr(sum(X[j,i] for j in subtour for i in subtour) <= len_sub - 1)
		model.update()
		cont += 1
	else:
		break
subtour.append(subtour[0])
bestdist = calcdist(subtour)

print("Solução: ", subtour)
print("Distância: ", bestdist)
print("Iterações: ", cont)
print("Tempo de execução: %s" % (time.time() - init))
printsolution(subtour)

print(" ")

with open('tempo.txt', 'r') as f:
    tempo = [[int(num) for num in line.split()] for line in f]
print(" ")
printtime(subtour)

