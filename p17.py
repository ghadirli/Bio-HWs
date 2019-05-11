import numpy as np

limbs = []


def initialize_matrix(npmatrix, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            npmatrix[i][j] = matrix[i][j]


def main():
    input_matrix = []
    n = int(input())
    for i in range(n):
        input_matrix.append([int(x) for x in input().split()])
    matrix = np.zeros((n, n), dtype=np.int32)
    initialize_matrix(matrix, input_matrix)
    calculate_limbs(input_matrix)
    edge, weight, _ = additive_phylogeny(matrix, n, n)
    for i in sorted(edge):
        for j in sorted(edge[i]):
            print("%d->%d:%d" % (i, j, weight[(i, j)]))


def limb(matrix, node):
    my_limb = float("inf")
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j != node and i != node:
                a = (matrix[i][node] + matrix[j][node] - matrix[i][j]) / 2
                if my_limb > a:
                    my_limb = a
    return int(my_limb)


def calculate_limbs(matrix):
    for i in range(len(matrix)):
        limbs.append(limb(matrix, i))


def additive_phylogeny(matrix, internal_nodes, n):
    if n == 2:
        return {1: [0], 0: [1]}, {(0, 1): matrix[0, 1], (1, 0): matrix[0, 1]}, internal_nodes
    limb_length = limb(matrix, n - 1)
    # reduce last row and last column
    for j in range(n - 1):
        matrix[j][n - 1] = matrix[j][n - 1] - limb_length
        matrix[n - 1][j] = matrix[j][n - 1]

    i, k = finding_two_leaves(matrix)
    # print("i and k are", i, k)
    x = matrix[i][n - 1]

    edges, weights, internal_nodes = additive_phylogeny(matrix[:-1, :-1], internal_nodes, n - 1)
    # print("weight is ", weight)
    i_near, k_near, i_x, n_x = find_path_in_tree(edges, weights, x, i, k)
    new_node = i_near

    if i_x != 0:
        new_node = internal_nodes
        internal_nodes += 1

        edges[i_near].remove(k_near)
        edges[k_near].remove(i_near)
        edges[i_near].append(new_node)
        edges[k_near].append(new_node)
        edges[new_node] = [i_near, k_near]

        weights[(new_node, i_near)] = weights[(i_near, new_node)] = i_x
        weights[(new_node, k_near)] = weights[(k_near, new_node)] = n_x
        del weights[(i_near, k_near)]
        del weights[(k_near, i_near)]

    edges[new_node].append(n - 1)
    edges[n - 1] = [new_node]
    weights[(n - 1, new_node)] = limb_length
    weights[(new_node, n - 1)] = limb_length
    return edges, weights, internal_nodes


def get_neighbours(tree, node):
    neighbours = []
    for i in range(len(tree[node])):
        if tree[node][i] != 0:
            neighbours.append(i)
    return neighbours


def find_path_in_tree(edge, weight, x, source, destination):
    # print("weight is ", weight)
    queue = [[source]]
    my_path = []
    visited = {source}

    while len(queue) > 0:
        path = queue.pop()
        node = path[-1]
        visited.add(node)
        if node == destination:
            my_path = path
            break
        for next_node in edge[node]:
            if next_node not in visited:
                queue.append(path + [next_node])
    distance = 0
    for k in range(len(my_path) - 1):
        i, j = my_path[k], my_path[k + 1]
        if distance + weight[(i, j)] > x:
            return i, j, x - distance, distance + weight[(i, j)] - x
        distance += weight[(i, j)]


def finding_two_leaves(matrix):
    length = matrix.shape[0]
    for i in range(length - 1):
        index = np.where(matrix[i] - matrix[-1] == matrix[i, -1])
        if len(index[0]) > 0:
            return index[0][0], i


if __name__ == '__main__':
    main()
