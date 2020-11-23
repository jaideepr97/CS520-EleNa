from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .mapAccessor import Graph, Node
import heapq
import math
from django.http import HttpResponse
import json
from .yens import compute_path_using_yens_with_elevation
from .a_star import getAstarRoute
from .djikstras import findShortestDistance
from .utilities import getClosestMappedNode 

G = Graph()

@csrf_exempt
def find_route(request):
	try:
		request = json.loads(request.body.decode("utf-8"))
	except:
		request = {
            "source_latitude": 1,
            "source_longitude": 1,
            "destination_latitude": 0,
            "destination_longitude": 0,
            "percentage": 10,
            "elevation_type": "min",
            "algorithm": "a_star"
        }
		pass
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
		maximizeElevationGain = True
	else:
		maximizeElevationGain = False
	
	closestSource = getClosestMappedNode(G, source)
	closestDestination = getClosestMappedNode(G, destination)
	shortest_distance = findShortestDistance(G, closestSource, closestDestination)
	data = dict()
	data['shortest_distance'] = shortest_distance 
	data['route'], data['elevation'], data['distance'] = selectAlgorithm(algorithm, source, destination, maximizeElevationGain, percentage, G, shortest_distance)
	
	return HttpResponse(json.dumps(data))

def selectAlgorithm(algorithm, source, destination, maximizeElevationGain, percentage, G, shortest_distance):
	closestSource = getClosestMappedNode(G, source)
	closestDestination = getClosestMappedNode(G, destination)
	if algorithm == "a_star":
		permissableDistance = (1 + (percentage/100))*shortest_distance
		return getAstarRoute(G, closestSource, closestDestination, maximizeElevationGain, permissableDistance)
	# if algorithm == "yens":
	# 	return compute_path_using_yens_with_elevation(G, closestSource, closestDestination, maximizeElevationGain, percentage)
