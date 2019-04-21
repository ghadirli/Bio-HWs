from Bio.SubsMat import MatrixInfo as blo

import my_utils
import p5

blosum = blo.blosum62

gap_opening = -11
inf = -500
gap_extension = -1
not_connected = -212


def print_shape(shape):
    x = int(len(shape) / 3)
    for i in range(len(shape)):
        print(shape[i])
        if i + 1 == x or i + 1 == 2 * x:
            print()


def main():
    v = input()
    w = input()
    graph = []
    shape = []
    construct_shape(shape, 3 * (len(w) + 1), len(v) + 1)
    construct_graph(graph, 3 * (len(w) + 1) * (len(v) + 1))
    initialize_graph(graph, shape, v, w)
    shape_length = int(len(shape) / 3)
    size = shape_length * len(shape[0])
    source = shape[0][0] + size
    sink = shape[shape_length - 1][len(shape[0]) - 1] + size
    k = get_best_path(source, sink, graph, shape)
    path = k[0]

    s = k[1]
    p5.print_path(path)
    print()
    print(s[sink])
    v_after = []
    w_after = []
    path = list(reversed(path))
    for i in range(len(path) - 1):
        x = path[i] % size
        y = path[i + 1] % size
        row = (x % len(shape[0]))

        column = int(x / len(shape[0]))
        if y - x == 1:
            v_after.append(v[row])
            w_after.append("-")
        if y - x == len(shape[0]):
            v_after.append("-")
            w_after.append(w[column])
        if y - x == len(shape[0]) + 1:
            v_after.append(v[row])
            w_after.append(w[column])
    v_after = ''.join(v_after)
    w_after = ''.join(w_after)
    print(v_after)
    print(w_after)


def get_best_path(source, sink, graph, shape):
    sorted_graph = p5.topological_sort(graph, not_connected)
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
    path_to_sink = []
    node = sink

    while node != source:
        path_to_sink.append(node)
        print("node is ", node)
        node = fathers[node]
    path_to_sink.append(source)
    return path_to_sink, s


def check_for_affine(grandfather, father, child, shape):
    if child - father == 1 and father - grandfather == 1:
        return True
    if child - father == len(shape[0]) and father - grandfather == len(shape[0]):
        return True
    return False


def construct_shape(shape, length, width):
    for i in range(length):
        row = []
        for j in range(width):
            row.append(i * width + j)
        shape.append(row)


def initialize_graph(graph, shape, v, w):
    shape_length = int(len(shape) / 3)
    size = shape_length * len(shape[0])

    # diagonal
    for i in range(shape_length, 2 * shape_length - 1):
        for j in range(len(shape[0]) - 1):
            node = shape[i][j] - size
            index_w = int(node / (len(shape[0])))
            index_v = int(node % (len(shape[0])))
            key = (v[index_v], w[index_w])
            if key not in blosum:
                key = (w[index_w], v[index_v])
            graph[shape[i][j]][shape[i + 1][j + 1]] = blosum[key]

    # horizontal
    for i in range(shape_length):
        for j in range(len(shape[0]) - 1):
            node = shape[i][j]
            graph[node][shape[i][j + 1]] = gap_extension

    # vertical
    for i in range(2 * shape_length, 3 * shape_length - 1):
        for j in range(len(shape[0])):
            node = shape[i][j]
            graph[node][shape[i + 1][j]] = gap_extension

    # from middle to upper
    for i in range(shape_length, 2 * shape_length):
        for j in range(len(shape[0]) - 1):
            node = shape[i][j]
            graph[node][shape[i][j + 1] - size] = gap_opening

    # from upper to middle
    for i in range(shape_length):
        for j in range(1, len(shape[0])):
            graph[shape[i][j]][shape[i][j] + size] = 0

    # from middle to lower
    for i in range(shape_length, 2 * shape_length - 1):
        for j in range(len(shape[0])):
            node = shape[i][j]
            graph[node][shape[i + 1][j] + size] = gap_opening

    # from lower to middle
    for i in range(2 * shape_length+1, 3 * shape_length):
        for j in range(len(shape[0])):
            graph[shape[i][j]][shape[i][j] - size] = 0


def construct_graph(graph, size):
    for i in range(size):
        row = []
        for j in range(size):
            row.append(not_connected)
        graph.append(row)


if __name__ == '__main__':
    main()
