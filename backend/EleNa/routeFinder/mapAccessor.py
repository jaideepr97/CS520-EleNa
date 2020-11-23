import osmnx as ox
from django.conf import settings
import pickle as pkl
import math
import heapq
import copy
import pickle as pkl


class Node:
    def __init__(self, latitude, longitude, elevation, osmid):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.osmid = osmid
        self.edges = []

    def addEdge(self, destination, length, destinationElevation):
        edge = Edge(destination, length, max((destinationElevation - self.elevation), 0))
        self.edges.append(edge)

    def removeEdge(self, destination):
        for edge in self.edges:
            if edge.destination == destination:
                self.edges.remove(edge)
                return

    def getEdge(self, destination):
        for edge in self.edges:
            if edge.destination == destination:
                return edge
        
class Graph:
    def __init__(self):
        self.G = ox.graph_from_place({'city': 'Amherst', 'state': 'MA', 'country': 'USA'}, network_type='all_private')
        # self.G = ox.graph_from_bbox(north=42.5140, south=42.2823, east=-72.2745, west=-72.8034, network_type='all_private')
        self.G = ox.elevation.add_node_elevations(self.G, 'AIzaSyCfA1DYkPDiQaYEIm4CucGcV_eF9W5c_xQ', 350, 0.02, 3)
        self.G = ox.add_edge_grades(self.G)
        self.nodes = self.initiateGraph()
        # filehandler = open("graph.pkl","wb")
        # pkl.dump(self,filehandler)
        # filehandler.close()

    def initiateGraph(self):
        nodes = {}
        for osmid in self.G.nodes():
            node = self.G.nodes[osmid]
            latitude, longitude = node['y'], node['x']
            node = Node(latitude, longitude, self.G.nodes[osmid]["elevation"], osmid)
            nodes[osmid] = node

        for edge in self.G.edges:
            source, destination, _ = edge
            edge_length = self.G.get_edge_data(source, destination)[0]['length']
            nodes[source].addEdge(destination, edge_length, nodes[destination].elevation)

        return nodes

    def getRouteElevation(self, route):
        routeElevation = 0
        for i in range (0, len(route)-1):
            routeElevation += self.nodes[route[i]].getEdge(route[i+1]).elevationGain
        return routeElevation


class Edge:
    def __init__(self, destination, length, elevationGain):
        self.destination = destination
        self.length = length
        self.elevationGain = elevationGain
