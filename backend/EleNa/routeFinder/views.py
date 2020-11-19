from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph, Node
import heapq
import math
from django.http import HttpResponse
import json
from .yens import compute_path_using_yens_with_elevation
from .a_star import binary_search_for_AStar
from .djikstras import findShortestDistance
from .utilities import getClosestMappedNode 

G = Graph()

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
	closestSource = getClosestMappedNode(G, source)
	closestDestination = getClosestMappedNode(G, destination)
	shortest_distance = findShortestDistance(G, closestSource, closestDestination)
	data = dict()
	data['shortest_distance'] = shortest_distance 
	data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, source, destination, is_min, percentage, G, shortest_distance)

	return HttpResponse(json.dumps(data))

def selectAlgorithm(algorithm, source, destination, is_min, percentage, G, shortest_distance):
	closestSource = getClosestMappedNode(G, source)
	closestDestination = getClosestMappedNode(G, destination)
	if algorithm == "a_star":
		# shortest_distance = findShortestDistance(G, closestSource, closestDestination)
		n_iters = 25
		return binary_search_for_AStar(G, closestSource, closestDestination, not is_min, (1 + percentage/100)*shortest_distance, n_iters)
	if algorithm == "yens":
		# shortest_distance = findShortestDistance(G, closestSource, closestDestination)
		return compute_path_using_yens_with_elevation(G, closestSource, closestDestination, is_min, percentage)


