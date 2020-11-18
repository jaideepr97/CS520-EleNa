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
            from_node, to_node, _ = edge
            edge_length = self.G.get_edge_data(from_node, to_node)[0]['length']
            nodes[from_node].add_edge(to_node, edge_length, nodes[to_node].elevation)

        return nodes

    # get elevation of path
    def get_path_elevation(self, path):
        total_elevation_gain = 0
        for i in range (0, len(path)-1):
            total_elevation_gain += self.nodes[path[i]].get_edge(path[i+1]).elevation_diff
        return total_elevation_gain

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
