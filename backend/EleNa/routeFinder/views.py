from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph
import heapq
import math
from django.http import HttpResponse
import json
# import .algorithms
from .yens import compute_path_using_yens_with_elevation
from .a_star import binary_search_for_AStar
from .djikstras import compute_shortest_distance 

@csrf_exempt
# Create your views here.
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

	if algorithm == 'yens':
		route, elevation, distance = get_yens_route(start_point, end_point, is_min, percentage, G)
		data['route'] = route
		data['elevation'] = elevation
		data['distance'] = distance
	if algorithm == 'a_star':
		route, elevation, distance = get_Astar_route(start_point, end_point, is_min, percentage, G)
		data['route'] = route
		data['elevation'] = elevation
		data['distance'] = distance

	return HttpResponse(json.dumps(data))
	# if algorithm == "a_star":
	# 	return get_Astar_route(source_latitude, source_longitude, destination_latitude, destination_longitude, elevation_type, percentage, G) 
	# elif algorithm == 'yens': 
	#     calculated_route, route_length, route_elevation =  get_yens_route(source_latitude, source_longitude, destination_latitude, destination_longitude, elevation_type, percentage, G) 
	# return None

# def access_map():
# 	return retrieve_map()

def get_Astar_route(start_point, end_point, is_min, dist_perc, custom_graph):
	n_iters = 25
	start_node = find_nearest_node(custom_graph, start_point[0], start_point[1])
	end_node = find_nearest_node(custom_graph, end_point[0], end_point[1])
	_, shortest_distance, _ = compute_shortest_distance(custom_graph, start_node, end_node)
	route, distance, elevation = binary_search_for_AStar(custom_graph, start_node, end_node, not is_min, (1 + dist_perc/100)*shortest_distance, n_iters)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

def get_yens_route(start_point, end_point, is_min, dist_perc, custom_graph):
	start_node = find_nearest_node(custom_graph, start_point[0], start_point[1])
	end_node = find_nearest_node(custom_graph, end_point[0], end_point[1])
	route, elevation, distance = compute_path_using_yens_with_elevation(custom_graph, start_node, end_node, is_min, dist_perc)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

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

