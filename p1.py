from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

def path_cost_comp(level, cellA, cellB):
    """ Computes the cost between cells

    Args:
        level: loaded level
        cellA: starting point
        cellB: ending point

    Returns:
        float of distance between cellA and cellB

    """
    if abs(cellA[0]-cellB[0]) == 1 and abs(cellA[1]-cellB[1]) == 1:
        distA = ((0.5 * sqrt(2)) * level['spaces'][cellA])
        distB = ((0.5 * sqrt(2)) * level['spaces'][cellB])
        dist = distA + distB
    else:
        distA = (0.5 * level['spaces'][cellA])
        distB = (0.5 * level['spaces'][cellB])
        dist = distA + distB
    return dist

def pq_sort(cell):
    """ Function to parse keys from tuples to sort queue

    Args:
        cell: tuple with distance as second element

    Returns:
        distance in tuple for sorting purposes

    """
    return cell[1]

def dijkstras_shortest_path(initial_position, destination, level, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """

    # Create empty dicts and queue
    dist = {}
    prev = {}
    queue = []

    # Push source onto queue
    heappush(queue, initial_position)
    dist[initial_position] = 0

    # Iterate while queue has elements, until destination is reached
    while len(queue) != 0:
        curr = heappop(queue)
        if curr == destination:
            path = []
            while curr != initial_position:
                path.append(curr)
                curr = prev[curr]
            path.append(curr)
            return path
        neighbors = navigation_edges(level, curr)
        neighbors.sort(key=pq_sort)

        # Iterate while there are still neighboring cells in neighbors list
        while len(neighbors) != 0:
            neighbor = neighbors.pop(0)
            cost = dist[curr] + neighbor[1]

            # If neighbor doesn't have dist, init, else compare to see if better cost
            if neighbor[0] not in dist:
                heappush(queue, neighbor[0])
                dist[neighbor[0]] = cost
                prev[neighbor[0]] = curr
            else:
                if cost < dist[neighbor[0]]:
                    dist[neighbor[0]] = cost
                    prev[neighbor[0]] = curr

def dijkstras_shortest_path_to_all(initial_position, level, adj):
    #TODO Dijkstras min cost to every cell in graph from initial_position
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    # Create empty dicts and queue
    dist = {}
    prev = {}
    queue = []

    # Push source onto queue
    heappush(queue, initial_position)
    dist[initial_position] = 0

    # Iterate while queue has elements, until destination is reached
    while len(queue) != 0:
        curr = heappop(queue)
        neighbors = navigation_edges(level, curr)

        # Iterate while there are still neighboring cells in neighbors list
        while len(neighbors) != 0:
            neighbor = neighbors.pop(0)
            cost = dist[curr] + neighbor[1]

            # If neighbor doesn't have dist, init, else compare to see if better cost
            if neighbor[0] not in dist:
                heappush(queue, neighbor[0])
                dist[neighbor[0]] = cost
                prev[neighbor[0]] = curr
            else:
                if cost < dist[neighbor[0]]:
                    dist[neighbor[0]] = cost
                    prev[neighbor[0]] = curr
    return dist


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    neighbors = []

    # Iterates in 8-way movement about center
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            neighbor = (cell[0]+x, cell[1]+y)
            if neighbor in level['spaces']:
                if neighbor != cell:
                    neighbors.append((neighbor, path_cost_comp(level, cell, neighbor)))
    #neighbors.sort(key=pq_sort)
    return neighbors


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)


    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        print("Path from " + src_waypoint + " to " + dst_waypoint + " found\n")
        show_level(level, path)

    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
	import sys
	#filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'
	_, filename, src_waypoint, dst_waypoint = sys.argv
    # Use this function call to find the route between two waypoints.
	test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
	cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
