import math
import heapq

def binary_search_for_AStar(G, source_node, destination_node, elevation_type, target_distance, iters):
        def get_distance_from_tgt_id(tgt_id):
            tgt_lat, tgt_lng = G.nodes[tgt_id].latitude, G.nodes[tgt_id].longitude
            distance_from_tgt = {}
            for node_id in G.nodes:
                curr_node = G.nodes[node_id]
                distance_from_tgt[node_id] = math.sqrt((curr_node.latitude - tgt_lat) ** 2
                                                       + (curr_node.longitude - tgt_lng) ** 2)
            return distance_from_tgt

        distance_from_tgt = get_distance_from_tgt_id(destination_node)
        start_weight, end_weight = 0, 1000000
        i = 0
        best_route = best_distance = None
        best_elevation = 0 if elevation_type == 'max' else 1000000000
        while (i < iters):
            curr_weight = (end_weight + start_weight) / 2
            if elevation_type == 'max':
                return_obj = AStar_maximize_elevationgain(G, source_node, destination_node, target_distance, distance_from_tgt,
                                                               curr_weight)
            else:
                return_obj = AStar_minimize_elevationgain(G, source_node, destination_node, target_distance, distance_from_tgt,
                                                               curr_weight)
            route, distance, elevation, is_valid = return_obj
            if elevation_type == 'max' and best_elevation < elevation and is_valid:
                best_route, best_distance, best_elevation = route, distance, elevation
            if elevation_type == 'min' and best_elevation > elevation and is_valid:
                best_route, best_distance, best_elevation = route, distance, elevation
            if is_valid == False:
                start_weight = curr_weight
            else:
                end_weight = curr_weight
            i += 1
        if best_route == None:
            best_route, best_distance, best_elevation = route, distance, elevation
        return best_route, best_distance, best_elevation

def AStar_minimize_elevationgain(G, src_id, tgt_id, distance_limit, distance_from_tgt, weight):
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
        temp_edges = G.nodes[old_id].edges
        for edge in temp_edges:
            new_id = edge.to_node
            if new_id in visited: continue
            new_distance = edge.length + distances[old_id]
            new_elevation = edge.elevation_diff + elevations[old_id]
            new_metric = new_elevation + weight * distance_from_tgt[new_id]
            #                 new_metric = weight * distance_from_tgt[new_id]
            if new_metric < a_star_metric.get(new_id, 1000000000):
                a_star_metric[new_id] = new_metric
                distances[new_id] = new_distance
                elevations[new_id] = new_elevation
                extending_from[new_id] = old_id
                heapq.heappush(heap, (new_metric, new_id))

    path = []
    to_add = tgt_id
    while (to_add != src_id):
        path.append(to_add)
        to_add = extending_from[to_add]
    path.append(src_id)
    return path[::-1], distances[tgt_id], elevations[tgt_id], distances[tgt_id] <= distance_limit

def AStar_maximize_elevationgain(self, src_id, tgt_id, distance_limit, distance_from_tgt, weight):
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
        temp_edges = self.nodes[old_id].edges
        for edge in temp_edges:
            new_id = edge.to_node
            if new_id in visited: continue
            new_distance = edge.length + distances[old_id]
            new_elevation = edge.elevation_diff + elevations[old_id]
            new_metric = new_elevation - weight * distance_from_tgt[new_id]
            #                 new_metric = - weight * distance_from_tgt[new_id]
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
