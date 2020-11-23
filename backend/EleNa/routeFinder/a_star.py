import math
import heapq

def getAstarRoute(graph, source, target, maximize_elevation, distance_limit):
	distanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target)
	start_weight, end_weight = 0, 1000000
	i = 0
	totalIterations = 35
	best_route = best_distance = None
	secondBestRoute = None
	secondBestDistance = None
	secondBestElevation = None
	closestToLimit = 1000000
	best_elevation = 0 if maximize_elevation else 1000000
	while (i < totalIterations):
		curr_weight = (end_weight + start_weight) / 2
		route, distance, elevation, is_valid  = AStar(graph, source, target, distance_limit, distanceFromTarget, curr_weight, maximize_elevation, elevationFromTarget)
		if (distance - distance_limit) < closestToLimit:
			secondBestRoute = route
			secondBestDistance = distance
			secondBestElevation = elevation
			closestToLimit = distance - distance_limit
		if maximize_elevation == True and best_elevation < elevation and is_valid:
			best_route, best_distance, best_elevation = route, distance, elevation
		if maximize_elevation == False and best_elevation > elevation and is_valid:
			best_route, best_distance, best_elevation = route, distance, elevation
		if is_valid == False:
			start_weight = curr_weight
		else:
			end_weight = curr_weight
		i += 1
	if best_route == None:
		# best_route, best_distance, best_elevation = route, distance, elevation
		best_route, best_distance, best_elevation = secondBestRoute, secondBestDistance, secondBestElevation

	
	calculatedRoute = []
	for osmid in best_route:
		node = graph.G.nodes[osmid]
		calculatedRoute.append([node['y'], node['x']])
	return calculatedRoute, best_elevation, best_distance


def AStar(graph, source, target, distance_limit, distanceFromTarget, weight, maximize_elevation, elevationFromTarget):
	heuristicScores = {}
	relativeElevationFromSource = {}
	routeDistanceFromSource = {}
	relativeElevationFromSource[source] = routeDistanceFromSource[source] = heuristicScores[source] = 0
	heap = [(0, source)]
	predecessors = {}
	visited = set()
	
	while (len(heap) > 0):
		# print(route)
		_, currentNode = heapq.heappop(heap)
		if currentNode == target: 
			break

		if currentNode in visited: 
			continue
		
		visited.add(currentNode)
		currentNodeEdges = graph.nodes[currentNode].edges
		for edge in currentNodeEdges:
			
			nextNode = edge.destination
			if nextNode in visited: 
				continue
			nextNodeRouteDistance = edge.length + routeDistanceFromSource[currentNode]
			nextNodeRelElevation = edge.elevationGain + relativeElevationFromSource[currentNode]
			
			if not maximize_elevation:
				heuristicScore = nextNodeRelElevation + weight * distanceFromTarget[nextNode]
				# heuristicScore =  nextNodeRelElevation + weight * getDistanceFromTargetWithElevation(distanceFromTarget[nextNode], elevationFromTarget[nextNode])
				if heuristicScore < heuristicScores.get(nextNode, 1000000000):
					heuristicScores[nextNode] = heuristicScore
					routeDistanceFromSource[nextNode] = nextNodeRouteDistance
					relativeElevationFromSource[nextNode] = nextNodeRelElevation
					predecessors[nextNode] = currentNode
					heapq.heappush(heap, (heuristicScore, nextNode))
					continue
			
			else:
				# heuristicScore = nextNodeRelElevation - weight * distanceFromTarget[nextNode]
				heuristicScore = nextNodeRouteDistance + nextNodeRelElevation - weight * getDistanceFromTargetWithElevation(distanceFromTarget[nextNode], elevationFromTarget[nextNode])
				if heuristicScore > heuristicScores.get(nextNode, -1000000000):
					heuristicScores[nextNode] = heuristicScore
					routeDistanceFromSource[nextNode] = nextNodeRouteDistance
					relativeElevationFromSource[nextNode] = nextNodeRelElevation
					predecessors[nextNode] = currentNode
					heapq.heappush(heap, (-heuristicScore, nextNode))
					continue

	route = []
	to_add = target
	while (to_add != source):
		route.append(to_add)
		to_add = predecessors[to_add]
	route.append(source)
	# return route[::-1], routeDistanceFromSource[target], relativeElevationFromSource[target], routeDistanceFromSource[target] <= distance_limit
	return route[::-1], routeDistanceFromSource[target], graph.getRouteElevation(route[::-1]), routeDistanceFromSource[target] <= distance_limit


def getDistanceFromTargetWithElevation(groundDistance, elevationDiff):
	return math.sqrt(math.pow(groundDistance,2) + math.pow(elevationDiff,2))

def getGroundDistanceAndElevationFromTarget(graph, target):
	elevationFromTarget = {}
	groundDistanceFromTarget = {}
	for osmid in graph.nodes:
		currentNode = graph.nodes[osmid]
		elevationFromTarget[osmid] = graph.nodes[target].elevation - currentNode.elevation
		groundDistanceFromTarget[osmid] = math.sqrt(math.pow((currentNode.latitude - graph.nodes[target].latitude), 2)
												+ math.pow((currentNode.longitude - graph.nodes[target].longitude), 2))
	return groundDistanceFromTarget, elevationFromTarget
