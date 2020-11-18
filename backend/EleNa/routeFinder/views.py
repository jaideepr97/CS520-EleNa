from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph, Node
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
	
	G = Graph()
	data = dict()
	data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, source, destination, is_min, percentage, G)

	return HttpResponse(json.dumps(data))

def selectAlgorithm(algorithm, source, destination, is_min, percentage, G):
	closestSource = getClosestMappedNode(G, source.latitude, source.longitude)
	closestDestination = getClosestMappedNode(G, destination.latitude, destination.longitude)
	if algorithm == "a_star":
		_, shortest_distance, _ = compute_shortest_distance(G, closestSource, closestDestination)
		n_iters = 25
		route, elevation, distance = binary_search_for_AStar(G, closestSource, closestDestination, not is_min, (1 + percentage/100)*shortest_distance, n_iters)
		return convert_route_to_latlong(route, G.G), elevation, distance
	if algorithm == "yens":
		route, elevation, distance = compute_path_using_yens_with_elevation(G, closestSource, closestDestination, is_min, percentage)
		return convert_route_to_latlong(route, G.G), elevation, distance

def convert_route_to_latlong(route, G):
	route_lnglat=[]
	for osid in route:
		node = G.nodes[osid]
		route_lnglat.append([node['y'], node['x']])
	return route_lnglat

def getClosestMappedNode(graph, lat, lng):
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

