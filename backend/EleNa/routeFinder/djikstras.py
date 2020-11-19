import heapq

# def compute_shortest_distance(graph, src_id, tgt_id):
#         min_distances = {}
#         elevations = {}
#         elevations[src_id] = 0
#         min_distances[src_id] = 0
#         heap = [(0, src_id)]
#         extending_from = {}
#         while (len(heap) > 0):
#             old_distance, old_id = heapq.heappop(heap)
#             if old_id == tgt_id: break
#             if min_distances.get(old_id, 1000000000) < old_distance: continue
#             temp_edges = graph.nodes[old_id].edges
#             for edge in temp_edges:
#                 new_distance = edge.length + old_distance
#                 new_elevation = edge.elevationGain + elevations[old_id]
#                 new_id = edge.destination
#                 if new_distance < min_distances.get(new_id, 1000000000):
#                     min_distances[new_id] = new_distance
#                     elevations[new_id] = new_elevation
#                     extending_from[new_id] = old_id
#                     heapq.heappush(heap, (new_distance, new_id))
#         path = []
#         to_add = tgt_id
#         while (to_add != src_id):
#             path.append(to_add)
#             to_add = extending_from[to_add]
#         path.append(src_id)
#         return path[::-1], min_distances[tgt_id], elevations[tgt_id]

def compute_shortest_distance(graph, source, destination):

    shortest_paths = {source: (None, 0)}
    current_node = source
    visited = set()
    
    while current_node != destination:
        visited.add(current_node)
        edges = graph.nodes[current_node].edges
        weight_to_current_node = shortest_paths[current_node][1]

        for edge in edges:
            next_node = edge.destination
            distance = edge.length + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, distance)
            else:
                current_shortest_distance = shortest_paths[next_node][1]
                if current_shortest_distance > distance:
                    shortest_paths[next_node] = (current_node, distance)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    return shortest_paths[destination][1]