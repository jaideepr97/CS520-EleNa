import osmnx as ox
from django.conf import settings
import pickle as pkl
import math
import heapq
import copy
from django.test import TestCase
import pickle
from .utilities import calcStraightLineDistance, getClosestMappedNode
from .a_star import binary_search_for_AStar, AStar, getDistanceFromTargetWithElevation, getGroundDistanceAndElevationFromTarget
from .djikstras import findShortestDistance
from .mapAccessor import Graph, Node
from .views import find_route


class QuestionModelTests(TestCase):
    def test_calcStraightLineDistance(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        self.assertIs(int(calcStraightLineDistance(gr.nodes[8099446119], gr.nodes[8099446119])), 0)

    def test_getClosestMappedNode(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        closestNode = getClosestMappedNode(gr, gr.nodes[8099446119])
        print(closestNode)
        self.assertIs(gr.nodes[8099446119].latitude, gr.nodes[closestNode].latitude)
        self.assertIs(gr.nodes[8099446119].longitude, gr.nodes[closestNode].longitude)

    def test_getGroundDistanceAndElevationFromTarget(self):
        infile = open('graph.pkl', 'rb')
        gr = pickle.load(infile)
        infile.close()
        # getGroundDistanceAndElevationFromTarget returns a tuple
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(gr, 8099446119)
        self.assertIs(int(groundDistanceFromTarget[8099446119]), 0)
        self.assertIs(int(elevationFromTarget[8099446119]), 0)

    def test_getDistanceFromTargetWithElevation(self):
        # self.assertIs((getDistanceFromTargetWithElevation(2,3)), math.sqrt(13))
        self.assertIs(int(getDistanceFromTargetWithElevation(2,3)), 3)

    def test_AStar_when_target_and_source_both_are_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, target_id, 10000, 10000, 100, -100, 100)
        print(paths, target_distance, target_elevation, distances)
        self.assertIs(int(target_distance), 0)
        self.assertIs(int(target_elevation), 0)
        self.assertIs(paths[0], target_id)

    def test_AStar_when_target_and_source_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 0
        source_id = 0
        
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, [10000], [100], [-100], [100])
        print(paths, target_distance, target_elevation, distances)
        self.assertIs(int(target_distance), 0)
        self.assertIs(int(target_elevation), 0)

    def test_AStar_when_target_and_source_diff_2_for_max(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 7278370352
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target_id)
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, groundDistanceFromTarget, 1, True, elevationFromTarget)
        self.assertIs(int(target_distance), 52)

    def test_AStar_when_target_and_source_diff_2_for_min(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 7278370352
        groundDistanceFromTarget, elevationFromTarget = getGroundDistanceAndElevationFromTarget(graph, target_id)
        paths, target_distance, target_elevation, distances = AStar(graph, target_id, source_id, 10000, groundDistanceFromTarget, 1, False, elevationFromTarget)
        self.assertIs(int(target_distance), 506)


    def test_binary_search_for_AStar(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        source_id = 8099446119
        maximize_elevation = 10000
        distance_limit = 10000
        iters = 2
        calculatedRoute, best_elevation, best_distance = binary_search_for_AStar(graph, source_id, target_id, maximize_elevation, distance_limit, iters)
        self.assertIs(int(best_elevation), 0)

    # def test_binary_search_for_AStar_when_diff(self):
    #     infile = open('graph.pkl', 'rb')
    #     graph = pickle.load(infile)
    #     infile.close()
    #     target_id = 8099446119
    #     source_id = 7278370346
    #     maximize_elevation = 10000
    #     distance_limit = 10000
    #     iters = 2
    #     calculatedRoute, best_elevation, best_distance = binary_search_for_AStar(graph, source_id, target_id, maximize_elevation, distance_limit, iters)
    #     self.assertNotEqual(int(best_elevation), 0)

    def test_dijkstra_findShortestDistance_when_source_dest_same(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 8099446119
        source_id = 8099446119
        self.assertIs(int(findShortestDistance(graph, source_id, target_id)), 0)

    def test_dijkstra_findShortestDistance_when_source_des_diff(self):
        infile = open('graph.pkl', 'rb')
        graph = pickle.load(infile)
        infile.close()
        target_id = 7278370349
        source_id = 7278370352
        self.assertIs(int(findShortestDistance(graph, source_id, target_id)), int(228))

    def test_graph_init(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(len(G)>0, True)

    def test_getRouteElevation(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(g.getRouteElevation([8099446119]), 0)

    def test_getRouteElevation(self):
        g = Graph()
        G = g.initiateGraph()
        self.assertIs(int(g.getRouteElevation([7278370346,7278370349])), int(3.25))

    def test_Node_addEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)

    def test_Node_removeEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)
        n.removeEdge(2)
        self.assertIs(len(n.edges)>0, False)

    def test_Node_getEdge(self):
        n = Node(1,1,1,1)
        self.assertIs(len(n.edges)>0, False)
        n.addEdge(2,2,2)
        self.assertIs(len(n.edges)>0, True)
        edge = n.getEdge(2)
        self.assertIs(edge.destination, 2)
    
    # def test_find_route(self):
    #     find_route()