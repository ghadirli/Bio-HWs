from collections import defaultdict

import my_utils

inf = -500
not_connected = -231


def main():
    k_mers = []
    while True:
        string = input()
        if string == "exit":
            break
        k_mers.append(string)

    graph = defaultdict(list)
    for i in range(len(k_mers)):
        graph[my_utils.prefix(k_mers[i])].append(my_utils.suffix(k_mers[i]))
    paths = maximal_non_branching_paths(graph)
    valid_paths = []
    for path in paths:
        if len(path) != 0:
            valid_paths.append(path)

    strings = get_paths(valid_paths, graph)

    for s in strings:
        print(s, end="\n")


def get_best_path(source, sink, graph, shape):
    sorted_graph = p1.topological_sort(graph, not_connected)
    z = sorted_graph.index(source)
    del sorted_graph[z]
    sorted_graph.insert(0, source)
    print(sorted_graph)
    s = [inf] * len(graph)
    s[source] = 0
    fathers = {}
    for i in range(len(sorted_graph)):
        if sorted_graph[i] == 72:
            print("hello")
        predecessors = my_utils.get_predecessors(graph, sorted_graph[i], not_connected)
        maximum = 0
        if len(predecessors) > 0:
            maximum = s[predecessors[0]] + graph[predecessors[0]][sorted_graph[i]]
            fathers[sorted_graph[i]] = predecessors[0]
        good_predecessors = False
        for j in range(len(predecessors)):
            if s[predecessors[j]] != inf:
                good_predecessors = True
        if i == 0:
            good_predecessors = True

        for j in range(len(predecessors)):

            if maximum < s[predecessors[j]] + graph[predecessors[j]][sorted_graph[i]] and s[predecessors[j]] != inf:
                maximum = s[predecessors[j]] + graph[predecessors[j]][sorted_graph[i]]
                fathers[sorted_graph[i]] = predecessors[j]

        if good_predecessors:
            s[sorted_graph[i]] = maximum
        else:
            s[sorted_graph[i]] = inf
        # print(s[sorted_graph[i]])
    path_to_sink = []
    node = sink

    while node != source:
        path_to_sink.append(node)
        print("node is ", node)
        node = fathers[node]
    path_to_sink.append(source)
    return path_to_sink, s


def find_isolated_cycles(graph):
    cycles = []
    visited = []
    for k in graph.items():
        if is_1_in_1_out(graph, k[0]) and k[0] not in visited:
            visited.append(k[0])
            cycles.append(get_cycle(graph, k[0], visited))
    return cycles


def get_cycle(graph, v, visited):
    w = v
    path = [w]
    while is_1_in_1_out(graph, w):
        visited.append(w)
        w = get_neighbours(graph, w)[0]
        path.append(w)
        if v == w:
            break
    if v == w:
        return path
    else:
        return []


def maximal_non_branching_paths(graph):
    paths = []
    for k in graph.items():
        if not is_1_in_1_out(graph, k[0]) and out_degree(graph, k[0]) > 0:
            paths.extend(path_from_node(graph, k[0]))
    return paths


def path_from_node(graph, v):
    paths = []
    for k in get_neighbours(graph, v):
        non_branching_path = [v]
        w = k
        non_branching_path.append(w)
        while is_1_in_1_out(graph, w):
            w = get_neighbours(graph, w)[0]
            non_branching_path.append(w)
        paths.append(non_branching_path)

    return paths


def generate_string(path, graph):
    string = path[0]
    for i in range(1, len(path)):
        string = string + path[i][len(path[i]) - 1]

    return string


def get_paths(paths, graph):
    strings = []
    for i in range(len(paths)):
        if len(paths[i]) != 0:
            s = generate_string(paths[i], graph)
            strings.append(s)
    return strings


def get_predecessors(graph, v):
    predecessors = []
    for k in graph.items():
        if v in k[1]:
            for i in range(k[1].count(v)):
                predecessors.append(k[0])
    return predecessors


def get_neighbours(graph, v):
    if v in graph:
        return graph[v]
    else:
        return []


def in_degree(graph, v):
    return len(get_predecessors(graph, v))


def out_degree(graph, v):
    return len(get_neighbours(graph, v))


def is_1_in_1_out(graph, v):
    if in_degree(graph, v) == 1 and out_degree(graph, v) == 1:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
