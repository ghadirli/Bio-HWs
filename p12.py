import re

import my_utils


def main():
    origins = []
    destinations = []
    while True:
        string = input()
        if string == "exit":
            break
        search = re.search("(\d+) -> (.+)", string)
        origins.append(int(search.group(1)))
        dests = list(search.group(2).split(","))
        dests = [int(x) for x in dests]
        destinations.append(dests)
    length = max(max([max(x) for x in destinations]), max(origins))
    graph = []
    # initialize graph with 0
    for i in range(length + 1):
        row = []
        for j in range(length + 1):
            row.append(0)
        graph.append(row)
    # complete graph
    for i in range(len(origins)):
        for j in range(len(destinations[i])):
            graph[origins[i]][destinations[i][j]] = 1
    graph_print(graph)
    paths = maximal_non_branching_paths(graph)
    paths.extend(find_isolated_cycles(graph))
    for i in range(len(paths)):
        if len(paths[i]) != 0:
            print_path(paths[i])


def print_path(path):
    for i in range(len(path)):

        print(path[i], end="")
        if i != len(path) - 1:
            print(" -> ", end="")
    print()


def find_isolated_cycles(graph):
    cycles = []
    visited = []
    for i in range(len(graph)):
        if my_utils.is_1_in_1_out(graph, i) and i not in visited:
            visited.append(i)
            cycles.append(get_cycle(graph, i, visited))
    return cycles



def get_cycle(graph, v, visited):
    w = v
    path = [w]
    while my_utils.is_1_in_1_out(graph, w):
        visited.append(w)
        w = my_utils.get_neighbours(graph, w)[0]
        path.append(w)
        if v == w:
            break
    if v == w:
        return path
    else:
        return []


def maximal_non_branching_paths(graph):
    paths = []
    for i in range(len(graph)):
        if not my_utils.is_1_in_1_out(graph, i) and my_utils.out_degree(graph, i) > 0:
            paths.extend(path_from_node(graph, i))
    return paths


def path_from_node(graph, v):
    paths = []

    for i in range(len(my_utils.get_neighbours(graph, v))):
        non_branching_path = [v]
        neighbours = my_utils.get_neighbours(graph, v)
        w = neighbours[i]
        non_branching_path.append(w)
        while my_utils.is_1_in_1_out(graph, w):
            w = my_utils.get_neighbours(graph, w)[0]
            non_branching_path.append(w)
        paths.append(non_branching_path)
        # if my_utils.is_1_in_1_out(graph, neighbours[i]):
        #     non_branching_path.extend(neighbours[i])

    return paths


def graph_print(graph):
    for i in range(len(graph)):
        print(graph[i])


if __name__ == '__main__':
    main()
