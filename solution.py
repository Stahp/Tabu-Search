import math
import matplotlib.pyplot as plt

def distance(a, b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def min_dist(actual_node, keys, nodes):
	min_dist= 10000000000000
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
	demands[int(items[0])]= int(items[1])
	i+= 1
i+=1
depot= int(lines[i].strip())
nodes_id= range(1, dimension+1)
routes= []
cost= 0
#start
route=[depot]
actual_capacity= 0
while True:
	# we make our current node the last visited node
	actual_node= route[len(route)-1]
	# keys will have only the nodes that haven't been visited yet: (demands= 0)
	keys= []
	for node in nodes_id:
		if demands[node]!=0:
			keys.append(node)
	# if we visited all the nodes we save our route and we add the distance back to the depot 
	if len(keys)==0:
		route.append(depot)
		routes.append(route)
		cost+= distance(nodes[actual_node], nodes[depot])
		break

	# we look for the closest node from our position
	dist, closest_node= min_dist(actual_node, keys, nodes)
	cost+= dist
	
	# if we can't hold more, we save our route, add the distance back to the depot and reset our new route and capacity
	if(demands[closest_node]+actual_capacity>capacity):
		route.append(depot)
		routes.append(route)
		route= [depot]
		cost+= distance(nodes[actual_node], nodes[depot])
		actual_capacity= 0

	# if we can hold more, we add the closest node to our route and add the demand to the capacity of the vehicule
	else:
		route.append(closest_node)
		actual_capacity+= demands[closest_node]
		demands[closest_node]= 0	#to mark this node as visited

print("The number of vehicles used are:")
print(len(routes))
print("The routes are:")
print(routes)
print("The cost is:")
print(cost)

x= []
y= []
for i in range(len(nodes_id)):
	a,b= nodes[nodes_id[i]]
	x.append(a)
	y.append(b)
	plt.annotate(i+1, xy= (a,b), xytext= (a, b+2))

plt.scatter(x, y, marker= "x")

for route in routes:
	routex= []
	routey= []
	for node in route:
		routex.append(nodes[node][0])
		routey.append(nodes[node][1])
	plt.plot(routex, routey)
plt.show()

