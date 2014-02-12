from random import *
import sys
from copy import *

n = 8
# chromosome is a bitstring, 1 means queen, 0 means no queen
q = [1 for i in range(n)] + [0 for i in range(n*n - n)]

def trans(x,y):
	# transform x,y coordinates to flat index
	return (y*n + x)

def fitness(q):
	# fitness function is the maximum sum of every
	maximum = 0
	f = 0
	# line,
	for i in range(0,n*n,n):
		lsum = sum(q[i:i+n])
		f += 0 if lsum <= 1 else lsum
	# column,
	for y in range(n):
		csum = 0
		index = y
		while index < n*n:
			csum += q[index]
			index += n
		f += 0 if csum <= 1 else csum
	# and diagonal
	# starting at top
	for start in range(n):
		y = 0
		x = start
		dsum = 0
		while x < n and y < n:
			dsum += q[trans(x,y)]
			x += 1
			y += 1
		f += 0 if dsum <= 1 else dsum
		x = 0
		y = start
		dsum = 0
		while y >= 0 and x < n:
			dsum += q[trans(x,y)]
			x += 1
			y -= 1
		f += 0 if dsum <= 1 else dsum
		x = start
		y = n-1
		dsum = 0
		while x < n and y >= 0:
			dsum += q[trans(x,y)]
			x += 1
			y -= 1
		f += 0 if dsum <= 1 else dsum
		x = start
		y = n-1
		dsum = 0
		while y >= 0 and x >= 0:
			dsum += q[trans(x,y)]
			x -= 1
			y -= 1
		f += 0 if dsum <= 1 else dsum
	return f

def randomqueen(q):
	# get the index of a random queen
	i = randint(0,n*n-1)
	direction = [1, -1][randint(0,1)]
	while True:
		if q[i]:
			return i
		i = (i + direction) % (n*n)

def mutate(q):
	# move a random queen in a random direction
	newboard = copy(q)
	rq = randomqueen(newboard)
	dir = [1,-1,n,-n,+1,-(n+1),n-1,-(n-1)][randint(0,7)]
	while newboard[(rq + dir) % (n*n)] == 1:
		dir = [1,-1,n,-n,+1,-(n+1),n-1,-(n-1)][randint(0,7)]
	newboard[rq] = 0
	newboard[(rq+dir)%(n*n)] = 1
	return newboard

def crossover(q1, q2):
	# "add" both bords and remove random queens
	# until there are only n left.
	nb = []
	for i in range(n*n):
		nb.append(int(q1[i] or q2[i]))
	while sum(nb) != n:
		nb[randomqueen(nb)] = 0
	return nb	

population = [(q,fitness(q))]
print(fitness(q))
generation = 0

for i in range(100):
	shuffle(q)
	population.append((copy(q),fitness(q)))


while True:
	print("generation",generation)
	generation += 1
	population = sorted(population, key=lambda x: x[1])

	newpop = []
	for i in range(10):
		for rr in range(9):
			m = mutate(population[i][0])
			f = fitness(m)
			if f == 0:
				print("found solution in generation",str(generation) + ": ")
				for x in range(0,n*n,n):
					print(m[x:x+n])
				sys.exit()
			newpop.append((m,f))
	for r in range(10):
		m = crossover(population[randint(0,10)][0], population[randint(0,10)][0])
		f = fitness(m)
		if f == 0:
			print("found solution in generation",str(generation) + ": ")
			for x in range(0,n*n,n):
				print(m[x:x+n])
			sys.exit()
		newpop.append((m,f))
	population = newpop

