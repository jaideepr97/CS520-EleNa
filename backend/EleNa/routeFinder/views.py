from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph
from .a_star import binary_search_for_AStar
import heapq
import math
from django.http import HttpResponse
import json

@csrf_exempt
# Create your views here.
def find_route(request):
	source_latitude = float(request.POST.get('source_latitude'))
	source_longitude = float(request.POST.get('source_longitude'))    
	destination_latitude = float(request.POST.get('destination_latitude'))
	destination_longitude = float(request.POST.get('destination_longitude'))
	percentage = int(request.POST.get('percentage'))
	elevation_type = request.POST.get('elevation_type')
	algorithm = request.POST.get('algorithm')
	start_point = (source_latitude, source_longitude)
	end_point = (destination_latitude, destination_longitude)
	if elevation_type == 'max':
		is_min = False
	else:
		is_min = True
	G = Graph()
	
	data = dict()

	print(start_point)
	print(end_point)
	print(algorithm)
	print(percentage)

	if algorithm == 'yens':
		route_yens, yens_elevation, yens_distance = get_yens_route(start_point, end_point, is_min, percentage, G)
		data['route_yens'] = route_yens
		data['yens_elevation'] = yens_elevation
		data['yens_distance'] = yens_distance
	if algorithm == 'a_star':
		route_astar, astar_elevation, astar_distance = get_Astar_route(start_point, end_point, is_min, percentage, G)
		data['route_astar'] = route_astar
		data['astar_elevation'] = astar_elevation
		data['astar_distance'] = astar_distance

	print("!!!!!!! returning data")
	print(data['route_astar'])
	return HttpResponse(json.dumps(data))
	# if algorithm == "a_star":
	# 	return get_Astar_route(source_latitude, source_longitude, destination_latitude, destination_longitude, elevation_type, percentage, G) 
	# elif algorithm == 'yens': 
	#     calculated_route, route_length, route_elevation =  get_yens_route(source_latitude, source_longitude, destination_latitude, destination_longitude, elevation_type, percentage, G) 
	# return None

# def access_map():
# 	return retrieve_map()

def get_Astar_route(start_point, end_point, is_min, dist_perc, custom_graph):
	print("IN ASTAR ROUTE")
	n_iters = 25
	start_node = custom_graph.find_nearest_node(start_point[0], start_point[1])
	end_node = custom_graph.find_nearest_node(end_point[0], end_point[1])
	_, shortest_distance, _ = custom_graph.compute_shortest_distance(start_node, end_node)
	route, distance, elevation = custom_graph.binary_search_for_AStar(start_node, end_node, not is_min, (1 + dist_perc/100)*shortest_distance, n_iters)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

def get_yens_route(start_point, end_point, is_min, dist_perc, custom_graph):
	start_node = custom_graph.find_nearest_node(start_point[0], start_point[1])
	end_node = custom_graph.find_nearest_node(end_point[0], end_point[1])
	route, elevation, distance = custom_graph.compute_path_using_yens_with_elevation(start_node, end_node, is_min, dist_perc)
	return convert_route_to_latlong(route, custom_graph.G), elevation, distance

# convert osmid in route to actual lat and long -> (lng, lat) in route_latlng
def convert_route_to_latlong(route, G):
	route_lnglat=[]
	for osid in route:
		node = G.nodes[osid]
		route_lnglat.append([node['x'], node['y']])
	return route_lnglat

