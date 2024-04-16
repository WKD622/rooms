from functools import reduce
from typing import List


def is_wall(vertex):
    return vertex in {'-', '+', '|', '/', '\\'}


def is_chair(vertex):
    return vertex in {'W', 'P', 'C', 'S'}


def print_a_result(result):
    print(f'{result["name"]}:')
    print(f'W: {result["W"]}, P: {result["P"]}, S: {result["S"]}, C: {result["C"]}')


def parse_room_name(coords, flat):
    name = []
    x, y = coords
    vertex = flat.content[y][x]
    while vertex != ")":
        name.append(vertex)
        x += 1
        vertex = flat.content[y][x]

    return ''.join(name)


def print_results(results: List):
    total_count = reduce(
        lambda a, b: {'W': a["W"] + b["W"], 'P': a["P"] + b["P"], 'C': a["C"] + b["C"], 'S': a["S"] + b["S"]},
        results
    )
    total_count["name"] = "total"
    print_a_result(total_count)

    for result in sorted(results, key=lambda x: x['name']):
        print_a_result(result)
