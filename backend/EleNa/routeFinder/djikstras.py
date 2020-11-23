
def findShortestDistance(graph, source, target):

    shortestDistanceDict = {source: (None, 0)}
    currentNode = source
    visited = set()
    
    while currentNode != target:
        visited.add(currentNode)
        edges = graph.nodes[currentNode].edges
        distanceToCurrentNode = shortestDistanceDict[currentNode][1]

        for edge in edges:
            destination = edge.destination
            distance = edge.length + distanceToCurrentNode
            if destination not in shortestDistanceDict:
                shortestDistanceDict[destination] = (currentNode, distance)
            else:
                currentShortestDistance = shortestDistanceDict[destination][1]
                if currentShortestDistance > distance:
                    shortestDistanceDict[destination] = (currentNode, distance)
        
        next_destinations = {node: shortestDistanceDict[node] for node in shortestDistanceDict if node not in visited}
        currentNode = min(next_destinations, key=lambda k: next_destinations[k][1])
        
    return shortestDistanceDict[target][1]