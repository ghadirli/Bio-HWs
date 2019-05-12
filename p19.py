maximum_node = 0


def main():
    matrix = []
    n = int(input())
    D = {}
    for i in range(n):
        matrix.append([int(x) for x in input().split()])
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            D[(i, j)] = matrix[i][j]
    max_node = n
    edge, weight = neighbour_joining(D, n, max_node)
    print(edge)
    print(weight)
    for i in sorted(edge):
        for j in sorted(edge[i]):
            print("%d->%d:%.3f" % (i, j, weight[(i, j)]))


def neighbour_joining(matrix, size, max_node):
    if size == 2:
        a = 0
        b = 0
        for key in matrix.keys():
            if key[0] != key[1]:
                a = key[0]
                b = key[1]
                break
        edge = {a: [b], b: [a]}
        weight = {(a, b): matrix[(a, b)], (b, a): matrix[(b, a)]}
        return edge, weight
    nj_matrix = neighbour_joining_matrix(matrix, size)
    i, j = find_non_diagonal_minimum(nj_matrix, size)
    print("i and j are", i, j)
    delta = (total_distance(matrix, i) - total_distance(matrix, j)) / (size - 2)
    limb_length_i = (matrix[(i, j)] + delta) / 2
    limb_length_j = (matrix[(i, j)] - delta) / 2
    add_new_row_col(matrix, i, j, max_node)
    max_node += 1
    size = size + 1
    matrix = remove_rows(matrix, i, j)
    matrix = remove_cols(matrix, i, j)
    size = size - 2
    edge, weight = neighbour_joining(matrix, size, max_node)

    add_two_nodes(edge, weight, limb_length_i, limb_length_j, i, j, max_node - 1)
    return edge, weight


def add_two_nodes(edge, weight, limb_length_i, limb_length_j, i, j, m):
    edge[i] = [m]
    edge[j] = [m]
    edge[m].append(i)
    edge[m].append(j)
    weight[(i, m)] = weight[(m, i)] = limb_length_i
    weight[(j, m)] = weight[(m, j)] = limb_length_j


def remove_cols(matrix, i, j):
    temp = {}
    for k in matrix.keys():
        if k[1] != i:
            temp[k] = matrix[k]
    temp1 = {}
    for k in temp.keys():
        if k[1] != j:
            temp1[k] = temp[k]
    return temp1


def remove_rows(matrix, i, j):
    temp = {}
    for k in matrix.keys():
        if k[0] != i:
            temp[k] = matrix[k]
    temp1 = {}
    for k in temp.keys():
        if k[0] != j:
            temp1[k] = temp[k]
    return temp1


def add_new_row_col(matrix, i, j, max_node):
    matrix[(max_node, max_node)] = 0
    s = set([i[0][0] for i in matrix.items()])
    for k in s:
        if k != max_node:
            matrix[(k, max_node)] = (matrix[(k, i)] + matrix[(k, j)] - matrix[(i, j)]) / 2
            matrix[(max_node, k)] = (matrix[(k, i)] + matrix[(k, j)] - matrix[(i, j)]) / 2


def find_non_diagonal_minimum(matrix, n):
    minimum = float("inf")
    min_index = None
    for i in matrix.items():
        if minimum > matrix[i[0]] != 0:
            minimum = matrix[i[0]]
            min_index = i[0]
    return min_index


def neighbour_joining_matrix(matrix, size):
    nj_matrix = initialize_with_zero(matrix)
    for i in nj_matrix.items():
        if i[0][0] != i[0][1]:
            nj_matrix[i[0]] = (size - 2) * matrix[i[0]] - total_distance(matrix, i[0][0]) - total_distance(matrix,
                                                                                                           i[0][1])
    return nj_matrix


def total_distance(matrix, i):
    s = 0
    for j in matrix.items():
        if j[0][0] == i:
            s += matrix[j[0]]
    return s


def initialize_with_zero(matrix):
    my_matrix = {}
    for i in matrix.items():
        my_matrix[i[0]] = 0

    return my_matrix


def print_matrix(matrix, n):
    for i in range(n):
        for j in range(n):
            if (i, j) in matrix:
                print(matrix[(i, j)], end=" ")
            else:
                print(" ", end=" ")
        print()


if __name__ == '__main__':
    main()
