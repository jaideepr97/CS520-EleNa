from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph
import heapq
import math
from django.http import HttpResponse
import json
from .yens import compute_path_using_yens_with_elevation
from .a_star import binary_search_for_AStar
from .djikstras import compute_shortest_distance 

@csrf_exempt
def find_route(request):
	request = json.loads(request.body)
	source_latitude = float(request["source_latitude"])
	source_longitude = float(request["source_longitude"])   
	destination_latitude = float(request["destination_latitude"])
	destination_longitude = float(request["destination_longitude"])
	percentage = int(request["percentage"])
	elevation_type = request["elevation_type"]
	algorithm = request["algorithm"]
	start_point = (source_latitude, source_longitude)
	end_point = (destination_latitude, destination_longitude)
	if elevation_type == 'max':
		is_min = False
	else:
		is_min = True
	G = Graph()
	
	data = dict()
	data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, start_point, end_point, is_min, percentage, G)

	return HttpResponse(json.dumps(data))

def selectAlgorithm(algorithm, start_point, end_point, is_min, percentage, G):
	start_node = find_nearest_node(G, start_point[0], start_point[1])
	end_node = find_nearest_node(G, end_point[0], end_point[1])
	if algorithm == "a_star":
		_, shortest_distance, _ = compute_shortest_distance(G, start_node, end_node)
		n_iters = 25
		route, elevation, distance = binary_search_for_AStar(G, start_node, end_node, not is_min, (1 + percentage/100)*shortest_distance, n_iters)
		return convert_route_to_latlong(route, G.G), elevation, distance
	if algorithm == "yens":
		route, elevation, distance = compute_path_using_yens_with_elevation(G, start_node, end_node, is_min, percentage)
		return convert_route_to_latlong(route, G.G), elevation, distance

# convert osmid in route to actual lat and long -> (lng, lat) in route_latlng
def convert_route_to_latlong(route, G):
	route_lnglat=[]
	for osid in route:
		node = G.nodes[osid]
		route_lnglat.append([node['y'], node['x']])
	return route_lnglat

def find_nearest_node(graph, lat, lng):
        temp_node = None
        min_distance = 1000000000
        for node_id in graph.nodes:
            node = graph.nodes[node_id]
            distance = (lat - node.latitude) ** 2 + (lng - node.longitude) ** 2
            distance = math.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
                temp_node = node.osmid
        return temp_node

