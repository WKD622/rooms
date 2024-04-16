from typing import Set, Tuple

from src.map import Map
from src.solutions.shared import is_wall, is_chair, parse_room_name, print_results


def generate_not_visited(width: int, height: int) -> Set:
    return {(x, y) for x in range(width) for y in range(height)}


def pick_a_vertex(vertices: Set):
    vertex = vertices.pop()
    return vertex


def recursively_explore_a_room(coords: Tuple[int, int],
                               flat,
                               visited: Set[Tuple[int, int]],
                               not_visited: Set[Tuple[int, int]],
                               result):
    visited.add(coords)

    # we have to use this if, because the first vertex is already taken from not_visited by pick_a_vertex function
    if coords in not_visited:
        not_visited.remove(coords)

    x, y = coords
    width, height = flat.get_dimensions()
    vertex = flat.content[y][x]

    # here I update the statistics about the room
    if is_chair(vertex):
        result[vertex] += 1

    # in case we encounter a start of a room name, we separately parse it
    if vertex == '(':
        result['name'] = parse_room_name((x + 1, y), flat)

    # and here are 4 ifs which move around the graph: right, bottom, left, up
    if (
            x + 1 < width
            and not is_wall(flat.content[y][x + 1])
            and (x + 1, y) not in visited
    ):  # move right
        recursively_explore_a_room((x + 1, y), flat, visited, not_visited, result)
    if (
            y - 1 > 0
            and not is_wall(flat.content[y - 1][x])
            and (x, y - 1) not in visited
    ):  # move down
        recursively_explore_a_room((x, y - 1), flat, visited, not_visited, result)
    if (
            x - 1 > 0
            and not is_wall(flat.content[y][x - 1])
            and (x - 1, y) not in visited
    ):  # move left
        recursively_explore_a_room((x - 1, y), flat, visited, not_visited, result)
    if (
            y + 1 < height
            and not is_wall(flat.content[y + 1][x])
            and (x, y + 1) not in visited
    ):  # move up
        recursively_explore_a_room((x, y + 1), flat, visited, not_visited, result)


def solution1(flat: Map):
    """
    The whole map is a graph, where each vertex represents one character from the map.

    Method:
    It draws a random vertex from not_visited vertices set until there are vertices in the set:
    a) if it's a wall then we just add it to visited vertices set and remove from not_visited set
    b) if it's a vertex inside a room (white space, chair, or anything else) we just recursively explore the room by
       spreading in all the directions (right, down, left, up) onto not visited vertices, meanwhile counting the chairs.
       While doing it we update visited and not_visited set. If we encounter a wall we don't spread in this direction.
       If we encounter a name of the room we parse it.
    """
    results = []
    width, height = flat.get_dimensions()

    not_visited = generate_not_visited(width, height)
    visited = set()

    # here we traverse the whole map
    while len(not_visited):
        x, y = pick_a_vertex(not_visited)
        vertex = flat.content[y][x]

        if is_wall(vertex):
            visited.add((x, y))
        else:
            result = {'W': 0, 'P': 0, 'C': 0, 'S': 0, 'name': None}
            recursively_explore_a_room((x, y), flat, visited, not_visited, result)
            if result['name'] is not None:  # we spawned inside a room
                results.append(result)

    print_results(results)
