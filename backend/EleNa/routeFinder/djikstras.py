import heapq

def compute_shortest_distance(graph, src_id, tgt_id):
        min_distances = {}
        elevations = {}
        elevations[src_id] = 0
        min_distances[src_id] = 0
        heap = [(0, src_id)]
        extending_from = {}
        while (len(heap) > 0):
            old_distance, old_id = heapq.heappop(heap)
            if old_id == tgt_id: break
            if min_distances.get(old_id, 1000000000) < old_distance: continue
            temp_edges = graph.nodes[old_id].edges
            for edge in temp_edges:
                new_distance = edge.length + old_distance
                new_elevation = edge.elevation_diff + elevations[old_id]
                new_id = edge.to_node
                if new_distance < min_distances.get(new_id, 1000000000):
                    min_distances[new_id] = new_distance
                    elevations[new_id] = new_elevation
                    extending_from[new_id] = old_id
                    heapq.heappush(heap, (new_distance, new_id))
        path = []
        to_add = tgt_id
        while (to_add != src_id):
            path.append(to_add)
            to_add = extending_from[to_add]
        path.append(src_id)
        return path[::-1], min_distances[tgt_id], elevations[tgt_id]