import copy
import heapq

def compute_path_using_yens_with_elevation(graph, src_id, tgt_id, is_min, dist_perc):
	copy_nodes = copy.deepcopy(graph.nodes)
	shortest, min_distance, min_distances = djikstras_for_yens(graph, copy_nodes,src_id,tgt_id)
	K_shortest = [(shortest, min_distance)]
	poten_k = []
	max_distance = min_distance + (min_distance*dist_perc/100)
	curr_dist = 0
	loop_count = 1
	while(True):
		for i in range(0, len(K_shortest[loop_count-1][0]) - 2):
			spur_node = K_shortest[loop_count - 1][0][i]
			root_path = K_shortest[loop_count - 1][0][0:i]
			for p in K_shortest:
				if root_path == p[0][0:i]:
					copy_nodes[p[0][i]].removeEdge(p[0][i+1])
			
			for node in root_path:
				del copy_nodes[node]

			spur_path, min_distance, extra = djikstras_for_yens(graph, copy_nodes, spur_node, tgt_id)
			if spur_path is not None:
				total_path = root_path + spur_path
				total_distance = min_distance + min_distances[spur_node] 
				if(total_path not in [i[0] for i in poten_k]):
					poten_k.append((total_path, total_distance))

			copy_nodes = copy.deepcopy(graph.nodes)
			if(len(poten_k)>10):
				break

		if len(poten_k) == 0:
			break
		poten_k.sort(key=lambda x:x[1])
		if (poten_k[0][1] > max_distance):
			break
		for pot in poten_k:
			if pot[1] <max_distance:
				K_shortest.append(pot)
		if(len(K_shortest) >10):
			break
		poten_k.pop()
		loop_count+=1
		if loop_count == 5:
			break

	best_route, elevation, distance = get_best_elevation_path_from_kshortest(graph, K_shortest, is_min)
	calculatedRoute = []
	for osmid in best_route:
		node = graph.G.nodes[osmid]
		calculatedRoute.append([node['y'], node['x']])
	return calculatedRoute, elevation, distance


# Shortest distance for yens 
def djikstras_for_yens(graph, nodes, src_id, tgt_id):
	min_distances = {}
	min_distances[src_id] = 0
	heap = [(0, src_id)]
	extending_from = {}
	while(len(heap)>0):
		old_distance, old_id = heapq.heappop(heap)
		if old_id == tgt_id: break
		if min_distances.get(old_id, 1000000000) < old_distance: continue
		temp_edges = nodes[old_id].edges
		for edge in temp_edges:
			if edge.destination not in nodes:
				continue
			new_distance = edge.length + old_distance
			new_id = edge.destination
			if new_distance < min_distances.get(new_id, 1000000000):
				min_distances[new_id] = new_distance
				extending_from[new_id] = old_id
				heapq.heappush(heap, (new_distance, new_id))
	path = []
	to_add = tgt_id
	while(to_add != src_id):
		path.append(to_add)
		if to_add not in extending_from:
			return None, None, None
		to_add = extending_from[to_add]
	path.append(src_id)
	return path[::-1], min_distances[tgt_id], min_distances


# return path with min/max elevation gain
def get_best_elevation_path_from_kshortest(graph, K_shortest, is_min):
	paths_with_elevation = []
	for var in K_shortest:
		path = var[0]
		total_elevation_gain = graph.getRouteElevation(path)
		paths_with_elevation.append((path, total_elevation_gain, var[1]))

	paths_with_elevation.sort(key=lambda x:x[1])
	if is_min:
		return paths_with_elevation[0]
	else:
		return paths_with_elevation[-1]