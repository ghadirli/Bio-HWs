from collections import defaultdict

inf = -500
not_connected = -123


def main():
    s1 = input()
    s2 = input()
    s3 = input()
    x_len = len(s1) + 1
    y_len = len(s2) + 1
    z_len = len(s3) + 1
    shape = construct_shape(x_len, y_len, z_len)
    graph = {}
    sink = shape[len(shape) - 1][len(shape[0]) - 1][len(shape[0][0]) - 1]
    initialize_graph(graph, shape, s1, s2, s3)
    sorted_graph = list(range(x_len * y_len * z_len))
    paths = get_best_path(0, x_len * y_len * z_len - 1, graph, sorted_graph)
    print(paths[1][sink])
    paths = list(reversed(paths[0]))

    produce_strings_from_path(paths, s1, s2, s3)


def produce_strings_from_path(path, s1, s2, s3):
    s1_after = []
    s2_after = []
    s3_after = []
    x_len = len(s1) + 1
    y_len = len(s2) + 1
    square = x_len * y_len
    for i in range(len(path) - 1):
        x_index = path[i] % x_len
        y_index = int((path[i] % square) / x_len)
        z_index = int(path[i]/square)
        x = path[i]
        y = path[i + 1]
        if y - x == 1:
            s2_after.append("-")
            s3_after.append("-")
            s1_after.append(s1[x_index])
        if y - x == x_len:
            s1_after.append("-")
            s3_after.append("-")
            s2_after.append(s2[y_index])
        if y - x == x_len + 1:
            s3_after.append("-")
            s2_after.append(s2[y_index])
            s1_after.append(s1[x_index])
        if y - x == square:
            s2_after.append("-")
            s1_after.append("-")
            s3_after.append(s3[z_index])
        if y - x == square + 1:
            s2_after.append("-")
            s1_after.append(s1[x_index])
            s3_after.append(s3[z_index])
        if y - x == square + x_len:
            s1_after.append("-")
            s2_after.append(s2[y_index])
            s3_after.append(s3[z_index])
        if y - x == square + x_len + 1:
            s1_after.append(s1[x_index])
            s2_after.append(s2[y_index])
            s3_after.append(s3[z_index])
    s1_after = ''.join(s1_after)
    s2_after = ''.join(s2_after)
    s3_after = ''.join(s3_after)
    print(s1_after)
    print(s2_after)
    print(s3_after)


def get_best_path(source, sink, graph, sorted_graph):
    s = [inf] * len(sorted_graph)
    s[source] = 0
    fathers = {}
    for i in range(len(sorted_graph)):

        predecessors = get_predecessors(graph, sorted_graph[i])
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
        node = fathers[node]
    path_to_sink.append(source)
    return path_to_sink, s


def get_predecessors(graph, v):
    predecessors = []
    for k in graph.items():
        if v in k[1]:
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


def initialize_graph(graph, shape, s1, s2, s3):
    z_len = len(shape)
    y_len = len(shape[0])
    x_len = len(shape[0][0])
    square = x_len * y_len
    for i in range(z_len - 1):
        for j in range(y_len - 1):
            for k in range(x_len - 1):
                graph[shape[i][j][k]] = {}
                graph[shape[i][j][k]][shape[i][j][k + 1]] = 0
                graph[shape[i][j][k]][shape[i + 1][j][k]] = 0
                graph[shape[i][j][k]][shape[i + 1][j][k + 1]] = 0
                graph[shape[i][j][k]][shape[i][j + 1][k]] = 0
                graph[shape[i][j][k]][shape[i][j + 1][k + 1]] = 0
                graph[shape[i][j][k]][shape[i + 1][j + 1][k]] = 0
                graph[shape[i][j][k]][shape[i + 1][j + 1][k + 1]] = 0

                if s1[(shape[i][j][k] % square) % x_len] == s2[int((shape[i][j][k] % square) / x_len)] == \
                        s3[int(shape[i][j][k] / square)]:
                    graph[shape[i][j][k]][shape[i + 1][j + 1][k + 1]] = 1

    for i in range(y_len - 1):
        for j in range(x_len - 1):
            graph[shape[z_len - 1][i][j]] = {}
            graph[shape[z_len - 1][i][j]][shape[z_len - 1][i + 1][j]] = 0
            graph[shape[z_len - 1][i][j]][shape[z_len - 1][i][j + 1]] = 0
            graph[shape[z_len - 1][i][j]][shape[z_len - 1][i + 1][j + 1]] = 0

    for i in range(z_len - 1):
        for j in range(y_len - 1):
            graph[shape[i][j][x_len - 1]] = {}
            graph[shape[i][j][x_len - 1]][shape[i + 1][j][x_len - 1]] = 0
            graph[shape[i][j][x_len - 1]][shape[i][j + 1][x_len - 1]] = 0
            graph[shape[i][j][x_len - 1]][shape[i + 1][j + 1][x_len - 1]] = 0

    for i in range(z_len - 1):
        for j in range(x_len - 1):
            graph[shape[i][y_len - 1][j]] = {}
            graph[shape[i][y_len - 1][j]][shape[i + 1][y_len - 1][j]] = 0
            graph[shape[i][y_len - 1][j]][shape[i][y_len - 1][j + 1]] = 0
            graph[shape[i][y_len - 1][j]][shape[i + 1][y_len - 1][j + 1]] = 0

    for i in range(z_len - 1):
        graph[shape[i][y_len - 1][x_len - 1]] = {}
        graph[shape[i][y_len - 1][x_len - 1]][shape[i + 1][y_len - 1][x_len - 1]] = 0
    for i in range(y_len - 1):
        graph[shape[z_len - 1][i][x_len - 1]] = {}
        graph[shape[z_len - 1][i][x_len - 1]][shape[z_len - 1][i + 1][x_len - 1]] = 0
    for i in range(x_len - 1):
        graph[shape[z_len - 1][y_len - 1][i]] = {}
        graph[shape[z_len - 1][y_len - 1][i]][shape[z_len - 1][y_len - 1][i + 1]] = 0

    return graph


def construct_shape(x_len, y_len, z_len):
    shape = []
    for i in range(z_len):
        square = []
        for j in range(y_len):
            row = []
            for k in range(x_len):
                row.append(x_len * y_len * i + x_len * j + k)
            square.append(row)
        shape.append(square)
    return shape


if __name__ == '__main__':
    main()
