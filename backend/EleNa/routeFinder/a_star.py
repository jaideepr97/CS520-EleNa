import math
import heapq

def binary_search_for_AStar(graph, src_id, tgt_id, maximize_elevation, distance_limit, iters):
	distance_from_tgt, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, tgt_id)
	start_weight, end_weight = 0, 1000000
	i = 0
	best_route = best_distance = None
	best_elevation = 0 if maximize_elevation else 1000000000
	while (i < iters):
		curr_weight = (end_weight + start_weight) / 2
		return_obj = AStar(graph, src_id, tgt_id, distance_limit, distance_from_tgt,
															curr_weight, maximize_elevation, elevationFromTarget)
		route, distance, elevation, is_valid = return_obj
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
		best_route, best_distance, best_elevation = route, distance, elevation
	
	calculatedRoute = []
	for osmid in best_route:
		node = graph.G.nodes[osmid]
		calculatedRoute.append([node['y'], node['x']])
	return calculatedRoute, best_elevation, best_distance


def AStar(graph, src_id, tgt_id, distance_limit, distance_from_tgt, weight, is_min, elevationFromTarget):
	a_star_metric = {}
	elevations = {}
	distances = {}
	elevations[src_id] = distances[src_id] = a_star_metric[src_id] = 0
	heap = [(0, src_id)]
	extending_from = {}
	visited = set()
	while (len(heap) > 0):
		_, old_id = heapq.heappop(heap)
		if old_id in visited: continue
		visited.add(old_id)
		if old_id == tgt_id: break
		temp_edges = graph.nodes[old_id].edges
		for edge in temp_edges:
			new_id = edge.destination
			if new_id in visited: continue
			new_distance = edge.length + distances[old_id]
			new_elevation = edge.elevationGain + elevations[old_id]
			
			if is_min:
				new_metric = new_elevation + weight * distance_from_tgt[new_id]
				# new_metric = new_distance + new_elevation + weight * getDistanceFromTargetWithElevation(distance_from_tgt[new_id], elevationFromTarget[new_id])

				if new_metric < a_star_metric.get(new_id, 1000000000):
					a_star_metric[new_id] = new_metric
					distances[new_id] = new_distance
					elevations[new_id] = new_elevation
					extending_from[new_id] = old_id
					heapq.heappush(heap, (new_metric, new_id))
			
			elif not is_min:
				new_metric = new_elevation - weight * distance_from_tgt[new_id]
				# new_metric = new_distance + new_elevation - weight * getDistanceFromTargetWithElevation(distance_from_tgt[new_id], elevationFromTarget[new_id])

				if new_metric > a_star_metric.get(new_id, -1000000000):
					a_star_metric[new_id] = new_metric
					distances[new_id] = new_distance
					elevations[new_id] = new_elevation
					extending_from[new_id] = old_id
					heapq.heappush(heap, (-new_metric, new_id))

	path = []
	to_add = tgt_id
	while (to_add != src_id):
		path.append(to_add)
		to_add = extending_from[to_add]
	path.append(src_id)
	return path[::-1], distances[tgt_id], elevations[tgt_id], distances[tgt_id] <= distance_limit
	# return path[::-1], distances[tgt_id], graph.getRouteElevation(path[::-1]), distances[tgt_id] <= distance_limit

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

# def get_distance_from_tgt_id(graph, tgt_id):
# 	tgt_lat, tgt_lng = graph.nodes[tgt_id].latitude, graph.nodes[tgt_id].longitude
# 	distance_from_tgt = {}
# 	for node_id in graph.nodes:
# 		curr_node = graph.nodes[node_id]
# 		distance_from_tgt[node_id] = math.sqrt((curr_node.latitude - tgt_lat) ** 2
# 												+ (curr_node.longitude - tgt_lng) ** 2)
# 	return distance_from_tgt