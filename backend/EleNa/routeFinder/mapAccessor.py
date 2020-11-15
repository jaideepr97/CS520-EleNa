import osmnx as ox
from django.conf import settings
import pickle as pkl
import math
import heapq
import copy
class Graph:
    def __init__(self):
        # self.G = ox.graph_from_bbox(north=42.5140, south=42.2823, east=-72.2745, west=-72.8034, network_type='drive')
        self.G = ox.graph_from_place({'city': 'Amherst', 'state': 'MA', 'country': 'USA'}, network_type='all_private')
        self.G = ox.elevation.add_node_elevations(self.G, 'AIzaSyCfA1DYkPDiQaYEIm4CucGcV_eF9W5c_xQ', 350, 0.02, 3)
        self.G = ox.add_edge_grades(self.G)
        self.nodes = self.construct_custom_graph()

    def construct_custom_graph(self):
        # with open("elevations.pkl", "rb") as fp:  # UnPickling
        #     elevations = pickle.load(fp)

        nodes = {}
        for node_id in self.G.nodes():
            osm_data = self.G.nodes[node_id]
            lat, lng = osm_data['y'], osm_data['x']
            # assert (lat, lng) in elevations
            # elevation = elevations[(lat, lng)]
            node = Node(lat, lng, self.G.nodes[node_id]["elevation"], node_id)
            nodes[node_id] = node

        for edge in self.G.edges:
            from_node, to_node, _ = edge
            edge_length = self.G.get_edge_data(from_node, to_node)[0]['length']
            nodes[from_node].add_edge(to_node, edge_length, nodes[to_node].elevation)

        return nodes

    def find_nearest_node(self, lat, lng):
        print("IN FIND NEAREST NODE")
        temp_node = None
        min_distance = 1000000000
        for node_id in self.nodes:
            node = self.nodes[node_id]
            distance = (lat - node.latitude) ** 2 + (lng - node.longitude) ** 2
            distance = math.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
                temp_node = node.osmid
        return temp_node

    def compute_shortest_distance(self, src_id, tgt_id):
        print("IN FIND SHORTEST DISTANCE")
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
            temp_edges = self.nodes[old_id].edges
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

    # Shortest distance for yens 
    def djikstras_for_yens(self, nodes, src_id, tgt_id):
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
                if edge.to_node not in nodes:
                    continue
                new_distance = edge.length + old_distance
                new_id = edge.to_node
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

    # get elevation of path
    def get_path_elevation(self, path):
        total_elevation_gain = 0
        for i in range (0, len(path)-1):
            total_elevation_gain += self.nodes[path[i]].get_edge(path[i+1]).elevation_diff
        return total_elevation_gain

    # return path with min/max elevation gain
    def get_best_elevation_path_from_kshortest(self, K_shortest, is_min):
        paths_with_elevation = []
        for var in K_shortest:
            path = var[0]
            total_elevation_gain = self.get_path_elevation(path)
            paths_with_elevation.append((path, total_elevation_gain, var[1]))

        paths_with_elevation.sort(key=lambda x:x[1])
        if is_min:
            return paths_with_elevation[0]
        else:
            return paths_with_elevation[-1]

    ''' 
    Yens k shortest paths for any k upto x% of shortest distance
    Algorithm from: https://en.wikipedia.org/wiki/Yen%27s_algorithm
    
    Description of function: Given a start(src_id) and an end location(tgt_id), 
    a route that maximizes or minimizes(is_min) elevation gain, while limiting 
    the total distance between the two locations to x%(dist_perc) of the shortest path.
    '''
    def compute_path_using_yens_with_elevation(self, src_id, tgt_id, is_min, dist_perc):
        copy_nodes = copy.deepcopy(self.nodes)
        shortest, min_distance, min_distances = self.djikstras_for_yens(copy_nodes,src_id,tgt_id)
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
                        copy_nodes[p[0][i]].remove_edge(p[0][i+1])
               
                for node in root_path:
                    del copy_nodes[node]

                spur_path, min_distance, extra = self.djikstras_for_yens(copy_nodes, spur_node, tgt_id)
                if spur_path is not None:
                    total_path = root_path + spur_path
                    total_distance = min_distance + min_distances[spur_node] 
                    if(total_path not in [i[0] for i in poten_k]):
                        poten_k.append((total_path, total_distance))

                copy_nodes = copy.deepcopy(self.nodes)
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
            print(len(K_shortest))
            if(len(K_shortest) >10):
                break
            poten_k.pop()
            loop_count+=1
            if loop_count == 5:
                break

        best_path, elevation, distance = self.get_best_elevation_path_from_kshortest(K_shortest, is_min)
        return best_path, elevation, distance

    def binary_search_for_AStar(self, src_id, tgt_id, maximize_elevation, distance_limit, iters):
        print("IN binary search for A STAR")
        def get_distance_from_tgt_id(tgt_id):
            tgt_lat, tgt_lng = self.nodes[tgt_id].latitude, self.nodes[tgt_id].longitude
            distance_from_tgt = {}
            for node_id in self.nodes:
                curr_node = self.nodes[node_id]
                distance_from_tgt[node_id] = math.sqrt((curr_node.latitude - tgt_lat) ** 2
                                                       + (curr_node.longitude - tgt_lng) ** 2)
            return distance_from_tgt

        distance_from_tgt = get_distance_from_tgt_id(tgt_id)
        start_weight, end_weight = 0, 1000000
        i = 0
        best_route = best_distance = None
        best_elevation = 0 if maximize_elevation else 1000000000
        while (i < iters):
            curr_weight = (end_weight + start_weight) / 2
            if maximize_elevation:
                return_obj = self.AStar_maximize_elevationgain(src_id, tgt_id, distance_limit, distance_from_tgt,
                                                               curr_weight)
            else:
                return_obj = self.AStar_minimize_elevationgain(src_id, tgt_id, distance_limit, distance_from_tgt,
                                                               curr_weight)
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
        return best_route, best_distance, best_elevation

    def AStar_minimize_elevationgain(self, src_id, tgt_id, distance_limit, distance_from_tgt, weight):
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
        print("IN AStar_maximize_elevationgain")        
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

class Node:
    def __init__(self, latitude, longitude, elevation, osmid):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.osmid = osmid
        self.edges = []

    def add_edge(self, to_node, length, to_elevation):
        edge = Edge(to_node, length, max(to_elevation - self.elevation, 0))
        self.edges.append(edge)

    def remove_edge(self, to_node):
        for edge in self.edges:
            if edge.to_node == to_node:
                self.edges.remove(edge)
                return
        return None

    def get_edge(self, to_node):
        for edge in self.edges:
            if edge.to_node == to_node:
                return edge
        return None

class Edge:
    def __init__(self, to_node, length, elevation_diff):
        self.to_node = to_node
        self.length = length
        self.elevation_diff = elevation_diff


# def retrieve_map():
#     G = osmnx.graph_from_place({'city': 'Amherst', 'state': 'MA', 'country': 'USA'}, network_type='all_private')
#     G = osmnx.elevation.add_node_elevations(G, settings.MAP_API_KEY, 350, 0.02, 3)
#     G = osmnx.add_edge_grades(G)
#     pkl.dump(G, open("amherst-graph.pkl", "wb"))
#     return G