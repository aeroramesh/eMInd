def generatePaths(theGraph, startNode, endNode, allPaths, pathSoFar=""):
    """
    Recursive function. Finds all paths through the specified
    graph from start node to end node. For cyclical paths, this stops
    at the end of the first cycle.
    """
    pathSoFar = pathSoFar + startNode

    for node in theGraph[startNode]:

        if node == endNode:
            allPaths.append(pathSoFar + node)
        else:
            generatePaths(theGraph, node, endNode, allPaths, pathSoFar)

graph = {"A":["B", "D", "E"], "B":["C"], "C":["D", "E"], "D":["C", "E"], "E":["B"]}
paths = []
generatePaths(graph, "C", "C", paths)
print(paths)