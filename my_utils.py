def get_predecessors(graph, v, not_connected):
    predecessors = []
    for i in range(len(graph)):
        if graph[i][v] != not_connected:
            predecessors.append(i)
    return predecessors


def get_neighbours(graph, v, not_connected):
    neighbours = []
    for i in range(len(graph[v])):
        if graph[v][i] != not_connected:
            neighbours.append(i)
    return neighbours


def in_degree(graph, v, not_connected):
    return len(get_predecessors(graph, v, not_connected))


def out_degree(graph, v, not_connected):
    return len(get_neighbours(graph, v, not_connected))


def prefix(string):
    return string[:len(string) - 1]


def suffix(string):
    return string[1:]


def is_1_in_1_out(graph, v, not_connected):
    if len(get_neighbours(graph, v, not_connected)) == 1 and len(get_predecessors(graph, v, not_connected)) == 1:
        return True
    else:
        return False


def print_graph(graph):
    for i in range(len(graph)):
        print(graph[i])
