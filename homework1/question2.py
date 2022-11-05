"""
helped by:
https://www.youtube.com/watch?v=oDqjPvD54Ss
https://www.geeksforgeeks.org/shortest-path-unweighted-graph/
"""
import doctest


def breadth_first_search(start, end, neighbor_function):
    """
    >>> breadth_first_search(start=(0,0), end=(5,-2), neighbor_function=four_neighbor_function)
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, -1), (5, -2)]
    >>> breadth_first_search(start=(0,0), end=(0,0), neighbor_function=four_neighbor_function)
    [(0, 0)]
    >>> breadth_first_search(start=(0,0), end=(-1,1), neighbor_function=four_neighbor_function)
    [(0, 0), (-1, 0), (-1, 1)]
    """
    queue = [start] # queue of all the nodes we need to check.
    visited = {start: None} # dictionary that contains all the node we checked and the parent node.
    while queue:
        node = queue.pop(0) # pop the first node of the queue.
        if node == end: # if we are reached our dest we start to build the path from the parent list.
            path = [node]
            while node != start:
                node = visited[node]
                path.insert(0, node)
            return path
        for neighbor in neighbor_function(node): # go through all the neighbors and if they have not visited so we add them to the queue.
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)
    raise Exception("There is no path.") # if we go through all the nieghbors and didn't found the dest.

def four_neighbor_function(node:any):
    (x,y) = node
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    
doctest.testmod(verbose=True)