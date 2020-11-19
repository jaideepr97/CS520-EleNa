import math

def getClosestMappedNode(graph, source):
    temp_node = None
    min_distance = 1000000000
    for osmid in graph.nodes:
        node = graph.nodes[osmid]
        distance = calcStraightLineDistance(source, node)
        if distance < min_distance:
            min_distance = distance
            temp_node = node.osmid
    return temp_node

def calcStraightLineDistance(source, destination):
    return math.sqrt( math.pow((destination.latitude - source.latitude),2) + math.pow((destination.longitude - source.longitude),2))
