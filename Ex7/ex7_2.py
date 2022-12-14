"""
I found two methods for cliques, one (find_cliques) returns all the cliques in a graph and the other (max_clique) returns the largest clique approximately,
I compare the clique to see if there is a difference between the accurate and the approximate.
it seems that there is no difference
helped by:
https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.clique.max_clique.html#networkx.algorithms.approximation.clique.max_clique
https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques
"""

import matplotlib.pyplot as plt
import networkx as nx
import random as rnd

def random_graph(n):
    p = rnd.uniform(0, 1)
    return nx.fast_gnp_random_graph(n, p)

def accurate_max_clique(graph):
    cliques = nx.find_cliques(graph)
    max_len = 0
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
    return max_len


def approximately_max_clique(graph):
    return len(nx.algorithms.approximation.clique.max_clique(graph))

def compare(graph):
    return accurate_max_clique(graph)/approximately_max_clique(graph)

def draw_diff(graph_size, comparation):
    plt.plot(graph_size, comparation)
    plt.xlabel('graph size')
    plt.ylabel('comparation')
    plt.show()


def run_test():
    graph_size = []
    comparation = []
    for n in range(50, 80):
        graph_size.append(n)
        graph = random_graph(n)
        comparation.append(compare(graph))
    draw_diff(graph_size, comparation)

run_test()