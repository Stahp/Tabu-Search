import math
import matplotlib.pyplot as plt
import timeit

#returns the route capacity
def routecapacity(route):
	capacity= 0
	for node in route:
		capacity+= demands[node]
	return capacity

#returns false is one of the routes has a capacity bigger than the vehicule capacity
def routes_isValid(routes):
	for route in routes:
		if routecapacity(route) > capacity:
			return False
	return True

#swap node a with node b
def swap_node(routes, a, b):
	newroutes= []
	for route in routes:
		tmp= []
		for node in route:
			if node==a:
				tmp.append(b)
			elif node==b:
				tmp.append(a)
			else:
				tmp.append(node)
		newroutes.append(tmp)
	return newroutes

# return the cost of the routes
def routeslength(routes):
	cost= 0
	for route in routes:
		for i in range(len(route)-1):
			cost+= distances[(route[i],route[i+1])]
	return cost

def getNeighbors(bestCandidate):
	Neighborhood= []
	for route in bestCandidate:
		for i in range(1, len(route)-1):
			for swapb in nodes_id[1:]:
				Neighbor= []
				Neighbor=swap_node(bestCandidate, route[i], swapb)
				if(routes_isValid(Neighbor)):
					Neighborhood.append(Neighbor)
	return Neighborhood

def distance(a, b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def min_dist(actual_node, keys, nodes):
	min_dist= 10000000
	closest_node= -1
	for key in keys:
		dist= distance(nodes[actual_node], nodes[key])
		if dist < min_dist:
			min_dist= dist
			closest_node= key
	return min_dist, closest_node

data= open("An39k5.vrp", "r")
lines= data.readlines()
nodes= {}
demands= {}
demands1= {}
i= 0
while "DIMENSION" not in lines[i]:
	i+=1
dimension= int(lines[i].split(" : ")[1])
while "CAPACITY" not in lines[i]:
	i+=1
capacity= int(lines[i].split(" : ")[1])
while "NODE_COORD_SECTION" not in lines[i]:
	i+=1
i+=1
while "DEMAND_SECTION" not in lines[i]:
	items= lines[i].strip().split()
	nodes[int(items[0])]= (int(items[1]), int(items[2]))
	i+= 1
i+=1

while "DEPOT_SECTION" not in lines[i]:
	items= lines[i].strip().split()
	demands1[int(items[0])]= int(items[1])
	demands[int(items[0])]= int(items[1])
	i+= 1
i+=1
depot= int(lines[i].strip())
nodes_id= range(1, dimension+1)
routes= []
#distances

distances= {}
for i in range(1,dimension+1):
	for j in range(1,dimension+1):
		if i!=j:
			distances[(i,j)]= distance(nodes[i], nodes[j])
			distances[(j,i)]= distances[(i,j)]

#start
route=[depot]
actual_capacity= 0
while True:
	# we make our current node the last visited node
	actual_node= route[len(route)-1]
	# keys will have only the nodes that haven't been visited yet: (demands= 0)
	keys= []
	for node in nodes_id:
		if demands1[node]!=0:
			keys.append(node)
	# if we visited all the nodes we save our route and we add the distance back to the depot 
	if len(keys)==0:
		route.append(depot)
		routes.append(route)
		break

	# we look for the closest node from our position
	dist, closest_node= min_dist(actual_node, keys, nodes)
	
	# if we can't hold more, we save our route, add the distance back to the depot and reset our new route and capacity
	if(demands1[closest_node]+actual_capacity>capacity):
		route.append(depot)
		routes.append(route)
		route= [depot]
		actual_capacity= 0

	# if we can hold more, we add the closest node to our route and add the demand to the capacity of the vehicule
	else:
		route.append(closest_node)
		actual_capacity+= demands1[closest_node]
		demands1[closest_node]= 0	#to mark this node as visited
cost= routeslength(routes)

print("The number of vehicles used are:")
print(len(routes))
print("The routes are:")
print(routes)
print("The cost is:")
print(cost)

#tabu algo

sBest= routes
sBestcost= cost
bestCandidate= routes
bestCandidatecost= cost
tabuList= []
tabuListLength= 20

start = timeit.default_timer()
timelimit= 5 #change this value to change timelimit in seconds

while True:
	Neighborhood= getNeighbors(bestCandidate)
	tabuList.append(bestCandidate)
	if(len(tabuList)>tabuListLength):
		tabuList= tabuList[1:]
	bestCandidate= []
	bestCandidatecost= 1000000
	for Neighbor in Neighborhood:
		Neighborcost= routeslength(Neighbor)
		if Neighbor not in tabuList:
			if Neighborcost < bestCandidatecost:
				bestCandidate= Neighbor
				bestCandidatecost= Neighborcost

	if bestCandidatecost < sBestcost:
		sBest= bestCandidate
		sBestcost= bestCandidatecost
	print("---------------")
	print("Best solution cost:")
	print(sBestcost)
	print("Best Candidate:")
	print(bestCandidate)
	print("Best Candidate Cost:")
	print(bestCandidatecost)
	stop = timeit.default_timer()
	if (stop - start)> timelimit:
		break

print("---------------")
print("---------------")
print("---------------")

print("The number of vehicles used are:")
print(len(sBest))
print("The routes are:")
print(sBest)
print("The cost is:")
print(sBestcost)


