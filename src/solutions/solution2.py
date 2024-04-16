from typing import Tuple, List

from src.map import Map
from src.solutions.shared import is_wall, is_chair, parse_room_name, print_results


def update_corners_to_stats(corners_to_stats, chair, room_corners):
    room_corners = sorted(room_corners, key=lambda k: [k[1], k[0]])
    corners_str = str(room_corners)
    if corners_str not in corners_to_stats:
        corners_to_stats[corners_str] = {'W': 0, 'P': 0, 'C': 0, 'S': 0}

    corners_to_stats[corners_str][chair] += 1


def is_corner(vertex: str) -> bool:
    return vertex == "+"


def go_up_until_finding_a_wall(coords: Tuple[int, int], flat) -> Tuple[int, int]:
    x, y = coords
    vertex = flat.content[y][x]
    while not is_wall(vertex) and y >= 0:
        y -= 1
        vertex = flat.content[y][x]

    return x, y


def find_the_next_wall_start(corner_coords: Tuple[int, int], previous_wall_relative_coords: Tuple[int, int],
                             flat: Map) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    possible_next_dx_dy = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    idx = possible_next_dx_dy.index(previous_wall_relative_coords)

    possible_dx_dy_in_the_right_direction_to_check = [*possible_next_dx_dy[idx + 1:], *possible_next_dx_dy[0: idx]]

    x, y = corner_coords
    for (dx, dy) in possible_dx_dy_in_the_right_direction_to_check:
        vertex = flat.content[y + dy][x + dx]
        if is_wall(vertex):
            return (x + dx, y + dy), (dx, dy)


def find_room_corners_recursively(coords: Tuple[int, int],
                                  direction: Tuple[int, int],
                                  flat: Map,
                                  room_corners: List[Tuple[int, int]]):
    """
    This function recursively crawls around the room's walls in a clockwise direction until it reaches the same corner
    for the second time. In the meantime it saves all the corners (their coordinates) into room_corners list.
    :param coords:
    :param direction:
    :param flat:
    :param room_corners:
    :return:
    """
    x, y = coords
    vertex = flat.content[y][x]

    # if it is a corner...
    if is_corner(vertex):

        # first we check if we had already visited this corner, if yes then it's a stop condition for our recursion
        if (x, y) in room_corners:
            return

        # if not then we have to remember our former crawling direction to find the right way to continue crawling.
        # We always have to make the first possible right turn.
        prev_dx, prev_dy = direction

        # here we find our new crawling direction
        (x, y), (dx, dy) = find_the_next_wall_start(coords, (-prev_dx, -prev_dy), flat)

        # we changed the wall only if dx and dy are different (sometimes there are corners on our way which are corners
        # for other rooms, but not for us, example:
        #
        # |   room  A   |
        # +------+------+
        #        | some other room
        #        |
        #
        # for example if we go along the horizontal line in the example from right to left, we cannot save the corner
        # in the middle as a corner of room A.
        if dx != prev_dx or dy != prev_dy:
            room_corners.append(coords)

        # since we found the new crawling direction we can now go and check out the next wall
        find_room_corners_recursively((x, y), (dx, dy), flat, room_corners)

    if is_wall(vertex) and not is_corner(vertex):
        # here we just crawl along the wall, we don't change the direction
        dx, dy = direction
        find_room_corners_recursively((x + dx, y + dy), (dx, dy), flat, room_corners)


def find_room_corners(starting_coords: Tuple[int, int], room_corners: List, flat: Map):
    """
    This function finds all corners of a room based on any vertex from its top wall,
    possible vertices of a top wall: '-', '/', '\'. It executes recursive function which crawls along the walls of a
    room in the clockwise direction.
    :param starting_coords:
    :param room_corners:
    :param flat:
    :return:
    """

    def compute_first_direction(vertex: str) -> Tuple[int, int]:
        # if it's an oblique wall ('/', '\', then we have to make different steps then when it's horizontal,
        # we always move clockwise
        if vertex == "/":
            return 1, -1
        if vertex == "-":
            return 1, 0
        if vertex == "\\":
            return 1, 1

    x, y = starting_coords
    dx, dy = compute_first_direction(flat.content[y][x])
    find_room_corners_recursively((x, y), (dx, dy), flat, room_corners)
    return room_corners


def solution2(flat: Map):
    """
    This solution is faster than solution 1 and takes less memory, but it's way more complex.

    It goes through a map from the top left corner to the bottom right.
    If it encounters a chair it goes up until it encounters a top wall of a room. Then it recursively crawls around the
    room along its walls in the clockwise direction and saves room's corners. It goes along walls of a room until it
    encounters the same corner twice.
    Thus, we know which chair belongs to which corners list (room). Based on the lists of corners of each room we can
    distinguish all rooms, and also we know which chair belong to which room.

    It also parses rooms' names with the same method. As it encounters '(' it goes all the way up until it reaches
    a top wall, and then it finds out all the corners which belong to the room where the name is.

    :param flat:
    :return:
    """
    width, height = flat.get_dimensions()
    corners_to_room_name = {}
    corners_to_stats = {}

    # we go through the map starting from the top left corner
    for i in range(height):
        for j in range(width):

            # if we have encountered a chair
            if is_chair(flat.content[i][j]):
                room_corners = []
                # we go up and return coords of the first encountered top wall vertex
                x, y = go_up_until_finding_a_wall((j, i), flat)

                # based on that vertex we find all corners of the room by going clockwise along the walls
                find_room_corners((x, y), room_corners, flat)

                # stats update
                update_corners_to_stats(corners_to_stats, flat.content[i][j], room_corners)

            # if we have encountered a room caption
            if flat.content[i][j] == '(':
                room_name = parse_room_name((j + 1, i), flat)
                room_corners = []
                # we go up and return coords of the first encountered top wall vertex
                x, y = go_up_until_finding_a_wall((j, i), flat)

                # based on that vertex we find all corners of the room by going clockwise along the walls
                find_room_corners((x, y), room_corners, flat)

                # stats update (we need to sort corners for later merging with corners_to_stats)
                corners_to_room_name[str(sorted(room_corners, key=lambda k: [k[1], k[0]]))] = room_name

    # merging to dicts to results
    results = []

    for key, val in corners_to_stats.items():
        room_name = corners_to_room_name[key]
        results.append({**val, 'name': room_name})

    print_results(results)
