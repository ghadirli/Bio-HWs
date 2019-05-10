def main():
    matrix = []
    n = int(input())
    for i in range(n):
        matrix.append([int(x) for x in input().split()])
    neighbour_joining(matrix, n)


def neighbour_joining(matrix, n):
    if n == 2:
        tree = [[0, matrix[0][1]], [matrix[0][1], 0]]
        return tree
    nj_matrix = neighbour_joining_matrix(matrix)
    i, j = find_non_diagonal_minimum(nj_matrix)
    delta = (total_distance(matrix, i) - total_distance(matrix, j)) / (n - 2)
    limb_length_i = (matrix[i][j] + delta) / 2
    limb_length_j = (matrix[i][j] - delta) / 2
    add_new_row_col(matrix, i, j)
    remove_rows(matrix, i, j)
    remove_cols(matrix, i, j)
    tree = neighbour_joining(matrix, n - 1)
    add_two_nodes(tree, limb_length_i, limb_length_j)
    return tree


def add_two_nodes(tree, limb_length_i, limb_length_j):
    tree.append([])
    tree.append([])
    for i in range(len(tree) - 2):
        tree[i].append(0)
        tree[i].append(0)
    for i in range(len(tree)):
        tree[len(tree) - 2].append(0)
        tree[len(tree) - 1].append(0)
    tree[len(tree) - 3][len(tree) - 2] = limb_length_i
    tree[len(tree) - 3][len(tree) - 1] = limb_length_j
    tree[len(tree) - 2][len(tree) - 3] = limb_length_i
    tree[len(tree) - 1][len(tree) - 3] = limb_length_j


def remove_cols(matrix, i, j):
    for k in range(len(matrix)):
        del matrix[k][i]
        del matrix[k][j]


def remove_rows(matrix, i, j):
    del matrix[i]
    del matrix[j]


def add_new_row_col(matrix, i, j):
    matrix.append([])
    for i in range(len(matrix)):
        matrix.append(0)
    m = len(matrix) - 1
    for k in range(len(matrix)):
        matrix[m][k] = matrix[k][m] = (matrix[k][i] + matrix[k][j] - matrix[i][j]) / 2


def find_non_diagonal_minimum(matrix):
    minimum = float("inf")
    min_index = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if minimum > matrix[i][j] != 0:
                minimum = matrix[i][j]
                min_index = (i, j)
    return min_index


def neighbour_joining_matrix(matrix):
    n = len(matrix)
    nj_matrix = initialize_with_zero(n)
    for i in range(len(nj_matrix)):
        for j in range(len(nj_matrix[0])):
            if i != j:
                nj_matrix[i][j] = (n - 2) * matrix[i][j] - total_distance(matrix, i) - total_distance(matrix, j)
    return nj_matrix


def total_distance(matrix, i):
    return sum(matrix[i])


def initialize_with_zero(n):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(n):
            matrix[i].append(0)
    return matrix


if __name__ == '__main__':
    main()
