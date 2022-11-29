"""
Q2
helped by:
https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/
https://github.com/LeviEyal/Algorithms-2-Course#%D7%9E%D7%A2%D7%91%D7%A8-%D7%A2%D7%9C-%D7%92%D7%A8%D7%A4%D7%99%D7%9D
https://networkx.org/documentation/stable/tutorial.html#adding-attributes-to-graphs-nodes-and-edges

in this question, I check if a graph is connected and how many connected components there are,
I did it with strategy design, the function can solve this with BFS and DFS algorithms and
can choose the output, the function support with networkx graph, and Graph_structure class.

Q3
https://www.codingame.com/training/hard/the-labyrinth
"""
import networkx as nx
import doctest


class Graph_structure:
    def __init__(self):
        self.G = {}

    def addNode(self, v):
        self.G[v] = {"visited": False, "neighbours": []}

    def addEdge(self, v, u):
        if v not in self.G or u not in self.G:
            raise Exception("one of the nodes not in the graph!")
        self.G[v]["neighbours"].append(u)
        self.G[u]["neighbours"].append(v)

    def getGraph(self):
        return self.G


gs = Graph_structure()
gs.addNode(0)
gs.addNode(1)
gs.addNode(2)
gs.addNode(3)
gs.addEdge(0, 1)
gs.addEdge(0, 2)
gs.addEdge(1, 2)
gs.addEdge(2, 3)

gs0 = Graph_structure()
gs0.addNode(0)
gs0.addNode(1)
gs0.addNode(2)
gs0.addNode(3)
gs0.addNode(4)
gs0.addNode(5)
gs0.addEdge(0, 1)
gs0.addEdge(0, 2)
gs0.addEdge(1, 2)
gs0.addEdge(4, 3)

NXG = nx.Graph()
NXG.add_node(0, visited=False)
NXG.add_node(1, visited=False)
NXG.add_node(2, visited=False)
NXG.add_node(3, visited=False)
edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
NXG.add_edges_from(edges)

NXG0 = nx.Graph()
NXG0.add_node(0, visited=False)
NXG0.add_node(1, visited=False)
NXG0.add_node(2, visited=False)
NXG0.add_node(3, visited=False)
NXG0.add_node(4, visited=False)
NXG0.add_node(5, visited=False)
edges = [(0, 1), (0, 2), (1, 2), (4, 3)]
NXG0.add_edges_from(edges)


def is_connected(algorithm: str, graph, output: str):
    """
    >>> is_connected(algorithm="BFS", graph=gs, output="isConnected")
    True
    >>> is_connected(algorithm="BFS", graph=NXG, output="isConnected")
    True

    >>> is_connected(algorithm="BFS", graph=gs, output="Connected_Components_num")
    1
    >>> is_connected(algorithm="BFS", graph=NXG, output="Connected_Components_num")
    1

    >>> is_connected(algorithm="DFS", graph=gs, output="isConnected")
    True
    >>> is_connected(algorithm="DFS", graph=NXG, output="isConnected")
    True

    >>> is_connected(algorithm="DFS", graph=gs, output="Connected_Components_num")
    1
    >>> is_connected(algorithm="DFS", graph=NXG, output="Connected_Components_num")
    1

    >>> is_connected(algorithm="BFS", graph=gs0, output="isConnected")
    False
    >>> is_connected(algorithm="BFS", graph=NXG0, output="isConnected")
    False

    >>> is_connected(algorithm="BFS", graph=gs0, output="Connected_Components_num")
    3
    >>> is_connected(algorithm="BFS", graph=NXG0, output="Connected_Components_num")
    3

    >>> is_connected(algorithm="DFS", graph=gs0, output="isConnected")
    False
    >>> is_connected(algorithm="DFS", graph=NXG0, output="isConnected")
    False

    >>> is_connected(algorithm="DFS", graph=gs0, output="Connected_Components_num")
    3
    >>> is_connected(algorithm="DFS", graph=NXG0, output="Connected_Components_num")
    3
    """

    # Checking the output str
    if not output == "isConnected" and not output == "Connected_Components_num":
        raise Exception("invalid output string!")

    # Checking the algorithm str
    if not algorithm == "BFS" and not algorithm == "DFS":
        raise Exception("invalid algorithm string!")

    # get visit flag for networkx graph
    def getVisitedNX(v):
        return graph.nodes[v]["visited"]

    # get visit flag for Graph_structure
    def getVisitedGraph(v):
        return graph[v]["visited"]

    # set visit flag for networkx graph
    def setVisitedNX(v, b):
        graph.nodes[v]["visited"] = b

    # set visit flag for Graph_structure
    def setVisitedGraph(v, b):
        graph[v]["visited"] = b

    # get all neighbors of a vertice for Graph_structure
    def getNeighboursGraph(v):
        return graph[v]["neighbours"]

    # get all neighbors of a vertice for networkx graph
    def getNeighboursNX(v):
        return list(graph.adj[v])

    # get all vertices for Graph_structure
    def getNodesGraph():
        return graph.keys()

    # get all vertices for networkx graph
    def getNodesNX():
        return list(graph.nodes)

    # check the graph type and set functions accordingly
    if isinstance(graph, Graph_structure):
        graph = graph.getGraph()
        commands = {"setVisited": setVisitedGraph,
                    "getVisited": getVisitedGraph, "getNeighbours": getNeighboursGraph, "getNodes": getNodesGraph}
    elif isinstance(graph, nx.classes.graph.Graph):
        commands = {"setVisited": setVisitedNX,
                    "getVisited": getVisitedNX, "getNeighbours": getNeighboursNX, "getNodes": getNodesNX}
    else:
        raise Exception("Graph is in valid!")

    # BFS
    def isConnectedBFS(v):
        commands["setVisited"](v, True)
        queue = []
        queue.append(v)
        while queue:
            s = queue.pop(0)
            for u in commands["getNeighbours"](s):
                if commands["getVisited"](u) == False:
                    commands["setVisited"](u, True)
                    queue.append(u)
    # DFS

    def isConnectedDFS(v):
        commands["setVisited"](v, True)
        for u in commands["getNeighbours"](v):
            if commands["getVisited"](u) == False:
                isConnectedDFS(u)

    # set algorithm functions
    operations = {"BFS": isConnectedBFS, "DFS": isConnectedDFS}

    # check connections
    counter = 0
    for v in commands["getNodes"]():
        commands["setVisited"](v, False)
    for v in commands["getNodes"]():
        if commands["getVisited"](v) == False:
            counter += 1
            operations[algorithm](v=v)

    # return by output
    if output == "isConnected":
        return True if counter == 1 else False
    else:
        return counter


doctest.testmod()
