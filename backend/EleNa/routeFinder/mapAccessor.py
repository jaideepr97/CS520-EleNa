import osmnx as ox
from django.conf import settings
import pickle as pkl
import math
import heapq
import copy
class Graph:
    def __init__(self):
        self.G = ox.graph_from_place({'city': 'Amherst', 'state': 'MA', 'country': 'USA'}, network_type='all_private')
        self.G = ox.elevation.add_node_elevations(self.G, settings.MAP_API_KEY, 350, 0.02, 3)
        self.G = ox.add_edge_grades(self.G)
        self.nodes = self.construct_custom_graph()

    def construct_custom_graph(self):
        nodes = {}
        for node_id in self.G.nodes():
            osm_data = self.G.nodes[node_id]
            lat, lng = osm_data['y'], osm_data['x']
            node = Node(lat, lng, self.G.nodes[node_id]["elevation"], node_id)
            nodes[node_id] = node

        for edge in self.G.edges:
            from_node, destination, _ = edge
            edge_length = self.G.get_edge_data(from_node, destination)[0]['length']
            nodes[from_node].add_edge(destination, edge_length, nodes[destination].elevation)

        return nodes

    # get elevation of path
    def get_path_elevation(self, path):
        total_elevation_gain = 0
        for i in range (0, len(path)-1):
            total_elevation_gain += self.nodes[path[i]].get_edge(path[i+1]).elevationGain
        return total_elevation_gain

class Node:
    def __init__(self, latitude, longitude, elevation, osmid):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.osmid = osmid
        self.edges = []

    def add_edge(self, destination, length, destinationElevation):
        edge = Edge(destination, length, (destinationElevation - self.elevation))
        self.edges.append(edge)

    def remove_edge(self, destination):
        for edge in self.edges:
            if edge.destination == destination:
                self.edges.remove(edge)
                return
        return None

    def get_edge(self, destination):
        for edge in self.edges:
            if edge.destination == destination:
                return edge
        return None

class Edge:
    def __init__(self, destination, length, elevationGain):
        self.destination = destination
        self.length = length
        self.elevationGain = elevationGain
