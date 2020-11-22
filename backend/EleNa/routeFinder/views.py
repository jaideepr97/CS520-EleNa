from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph, Node
import heapq
import math
from django.http import HttpResponse
import json
# from .yens import compute_path_using_yens_with_elevation
# from .a_star import binary_search_for_AStar
# from .djikstras import findShortestDistance
# from .utilities import getClosestMappedNode 

# G = Graph()
custom_graph = Graph() 

@csrf_exempt
def find_route(request):
	request = json.loads(request.body)
	sourceLatitude = float(request["source_latitude"])
	sourceLongitude = float(request["source_longitude"])   
	destinationLatitude = float(request["destination_latitude"])
	destinationLongitude = float(request["destination_longitude"])
	percentage = int(request["percentage"])
	elevationType = request["elevation_type"]
	algorithm = request["algorithm"]

	source = Node(sourceLatitude, sourceLongitude, None, None)
	destination = Node(destinationLatitude, destinationLongitude, None, None)

	if elevationType == 'max':
		is_min = False
	else:
		is_min = True
	
	# G = Graph()
	# closestSource = getClosestMappedNode(G, source)
	# closestDestination = getClosestMappedNode(G, destination)
	# shortest_distance = findShortestDistance(G, closestSource, closestDestination)
	data = dict()
	# data['shortest_distance'] = shortest_distance 
	# data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, source, destination, is_min, percentage, G, shortest_distance)



	if algorithm == 'D':
		route_shortest, shortest_elevation, shortest_distance = get_route(source, destination, custom_graph)
		data['route'] = route_shortest
		data['elevation'] = shortest_elevation
		data['distance'] = shortest_distance
	if algorithm == 'yens':
		route_yens, yens_elevation, yens_distance = get_yens_route(source, destination, is_min, percentage, custom_graph)
		data['route'] = route_yens
		data['elevation'] = yens_elevation
		data['distance'] = yens_distance
	if algorithm == 'a_star':
		route_astar, astar_elevation, astar_distance = get_Astar_route(source, destination, is_min, percentage, custom_graph)
		data['route'] = route_astar
		data['elevation'] = astar_elevation
		data['distance'] = astar_distance
	
	return HttpResponse(json.dumps(data))

# def selectAlgorithm(algorithm, source, destination, is_min, percentage, G, shortest_distance):
# 	closestSource = getClosestMappedNode(G, source)
# 	closestDestination = getClosestMappedNode(G, destination)
# 	if algorithm == "a_star":
# 		# shortest_distance = findShortestDistance(G, closestSource, closestDestination)
# 		n_iters = 25
# 		return binary_search_for_AStar(G, closestSource, closestDestination, not is_min, (1 + percentage/100)*shortest_distance, n_iters)
# 	if algorithm == "yens":
# 		# shortest_distance = findShortestDistance(G, closestSource, closestDestination)
# 		return compute_path_using_yens_with_elevation(G, closestSource, closestDestination, is_min, percentage)






# return route given start and end point -> (lat, lng)
def get_route(start_point, end_point, custom_graph):
	start_node = custom_graph.find_nearest_node(start_point.latitude, start_point.longitude)
	end_node = custom_graph.find_nearest_node(end_point.latitude, end_point.longitude)
	route, distance, elevation = custom_graph.compute_shortest_distance(start_node, end_node)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

def get_Astar_route(start_point, end_point, is_min, dist_perc, custom_graph):
	n_iters = 25
	start_node = custom_graph.find_nearest_node(start_point.latitude, start_point.longitude)
	end_node = custom_graph.find_nearest_node(end_point.latitude, end_point.longitude)
	_, shortest_distance, _ = custom_graph.compute_shortest_distance(start_node, end_node)
	route, distance, elevation = custom_graph.binary_search_for_AStar(start_node, end_node, not is_min, (1 + dist_perc/100)*shortest_distance, n_iters)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

def get_yens_route(start_point, end_point, is_min, dist_perc, custom_graph):
	start_node = custom_graph.find_nearest_node(start_point.latitude, start_point.longitude)
	end_node = custom_graph.find_nearest_node(end_point.latitude, end_point.longitude)
	route, elevation, distance = custom_graph.compute_path_using_yens_with_elevation(start_node, end_node, is_min, dist_perc)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

# convert osmid in route to actual lat and long -> (lng, lat) in route_latlng
def convert_route_to_latlong(route, G):
	route_lnglat=[]
	for osid in route:
		node = G.nodes[osid]
		route_lnglat.append([node['x'], node['y']])
	return route_lnglat