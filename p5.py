import re

import my_utils

const = -100
inf = -500



def main():
    source = int(input())
    sink = int(input())
    graph = []

    origins = []
    dests = []
    values = []
    while True:
        string = input()
        if string == "exit":
            break
        str_search = re.search('(\d+)->(\d+):(\d+)', string)
        origins.append(int(str_search.group(1)))
        dests.append(int(str_search.group(2)))
        values.append(int(str_search.group(3)))

    maximum_node = max(max(origins), max(dests)) + 1
    for i in range(maximum_node):
        row = []
        for j in range(maximum_node):
            row.append(0)
        graph.append(row)
    for i in range(len(origins)):
        graph[origins[i]][dests[i]] = values[i]

    print(get_best_path(source, sink, graph)[1][sink])

    print_path(get_best_path(source, sink, graph)[0])


def print_path(path):
    for i in range(len(path) - 1, -1, -1):
        print(path[i], end="->")


def get_best_path(source, sink, graph):
    sorted_graph = topological_sort(graph, -222)

    z = sorted_graph.index(source)
    del sorted_graph[z]
    sorted_graph.insert(0, source)
    s = [inf] * len(graph)
    s[source] = 0
    fathers = {}
    for i in range(len(sorted_graph)):
        predecessors = get_predecessors(graph, sorted_graph[i])
        maximum = 0
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

    path_to_sink = []
    node = sink

    while node != source:
        path_to_sink.append(node)
        print(node)
        node = fathers[node]
    path_to_sink.append(source)
    return path_to_sink, s


def get_predecessors(graph, v):
    predecessors = []
    for i in range(len(graph)):
        if graph[i][v] != 0:
            predecessors.append(i)
    return predecessors


def get_neighbours(graph, v):
    neighbours = []
    for i in range(len(graph[v])):
        if graph[v][i] != 0:
            neighbours.append(i)
    return neighbours


# adapted from geeksforgeeks
def topological_sort(graph, not_connected):
    visited = [False] * (len(graph))
    stack = []

    for i in range(len(graph)):
        if not visited[i]:
            topological_util(graph, visited, i, stack, not_connected)

    return stack


def topological_util(graph, visited, v, stack, not_connected):
    visited[v] = True

    for i in my_utils.get_neighbours(graph, v, not_connected):
        if not visited[i]:
            topological_util(graph, visited, i, stack, not_connected)

    stack.insert(0, v)


def get_column(graph, i):
    return [row[i] for row in graph]


if __name__ == '__main__':
    main()
