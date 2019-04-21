import re


def main():
    string = []
    our_input = "input"
    while True:
        our_input = input()
        if our_input == "exit":
            break
        string.append(our_input)

    graph = []

    for i in range(len(string)):
        search = re.search("(\d+) -> (.+)", string[i])
        node = int(search.group(1))
        neighbours = list(search.group(2).split(","))
        # print(neighbours)
        neighbours = [int(x) for x in neighbours]
        row = [0] * (max(neighbours) + 1)

        for neighbour in neighbours:
            row[neighbour] = 1
        if len(graph) <= node:
            insert_row(graph, row, node)
        else:
            graph[node] = row

    maximum = 0
    for i in range(len(graph)):
        if len(graph[i]) > maximum:
            maximum = len(graph[i])

    size = max(maximum, len(graph))
    for i in range(len(graph)):
        for j in range(len(graph[i]), size):
            graph[i].append(0)

    # print_graph(graph)

    start = None
    end = None
    for i in range(size):
        res = sum(get_column(graph, i)) - sum(graph[i])
        if res == 1:
            end = i
        if res == -1:
            start = i
    graph[end][start] = 1
    path = find_eulerian_path(graph, start)
    index = 0
    print("path is ", path)
    for i in range(len(path)):
        if path[i] == end and path[(i + 1) % len(path)] == start:
            index = i
            break
    print(path[index+1:])
    print(path[:index])
    true_path = path[index+1:] + path[:index+1]
    # x = true_path.pop(0)
    # true_path.append(x)
    print(true_path)
    for i in range(len(true_path)):
        print(true_path[i], end="->")


def no_edges(graph):
    edges = 0
    for i in range(len(graph)):
        edges += sum(graph[i])
    return edges


def find_eulerian_path(graph, start):
    temp_graph = graph.copy()
    temp_stack = []
    path_stack = []

    temp_stack.insert(0, start)
    # print_graph(temp_graph)
    while True:
        current = temp_stack[0]
        if sum(temp_graph[current]) == 0:
            path_stack.insert(0, temp_stack.pop(0))
        if sum(temp_graph[current]) != 0:
            node = temp_graph[current].index(1)
            temp_graph[current][node] = 0
            temp_stack.insert(0, node)

        if len(temp_stack) == 0:
            break
    path_stack.pop(len(path_stack)-1)
    return path_stack


def get_column(graph, i):
    return [row[i] for row in graph]


def print_graph(graph):
    for i in range(len(graph)):
        print(graph[i])


def insert_row(graph, row, node):
    for i in range(len(graph), node):
        graph.append([])
    graph.append(row)


def insert(row, i):
    for i in range(len(row), i):
        row.append(0)
    row.append(1)


if __name__ == '__main__':
    main()
