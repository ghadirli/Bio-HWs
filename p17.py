zero_connect = 5983
limbs = []


def main():
    matrix = []
    n = int(input())
    for i in range(n):
        matrix.append([int(x) for x in input().split()])
    calculate_limbs(matrix)
    print(additive_phylogeny(matrix))


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


def additive_phylogeny(matrix):
    n = len(matrix)
    if n == 2:
        return [[0, matrix[0][1]], [matrix[0][1], 0]]
    limb_length = limbs[n - 1]
    for j in range(n - 1):
        matrix[j][n - 1] = matrix[j][n - 1] - limb_length
        matrix[n - 1][j] = matrix[j][n - 1]
    i, k = finding_two_leaves(matrix, n - 1)
    print("i and k are", i, k)
    x = matrix[i][n - 1]
    matrix = remove_last_col_and_row(matrix)
    tree = additive_phylogeny(matrix)
    v = find_node_with_distance_from_source(tree, i, k, x)
    print("v is ", v, "matrix is ", matrix)
    tree = add_node(tree, v, limb_length)
    return tree


def get_neighbours(tree, node):
    neighbours = []
    for i in range(len(tree[node])):
        if tree[node][i] != 0:
            neighbours.append(i)
    return neighbours


def find_path_in_tree(source, destination, tree):
    queue = [[source]]
    visited = set([source])
    my_path = []

    while len(queue) > 0:
        path = queue.pop()
        node = path[-1]
        visited.add(node)
        if node == destination:
            my_path = path
            break
        for next_node in get_neighbours(tree, node):
            if next_node not in visited:
                queue.append(path + [next_node])
    return my_path


def find_node_with_distance_from_source(tree, source, destination, distance):
    path = find_path_in_tree(source, destination, tree)
    print("path is ", path)
    cost = 0
    for i in range(1, len(path)):
        cost += tree[path[i - 1]][path[i]]
        if cost == distance:
            return path[i]


def add_node(tree, v, limb_length):
    for i in range(len(tree)):
        tree[i].append(0)
    tree.append([0] * len(tree[0]))
    tree[len(tree) - 1][v] = limb_length
    tree[v][len(tree) - 1] = limb_length

    return tree


def remove_last_col_and_row(matrix):
    temp = []
    for i in range(len(matrix) - 1):
        temp.append([])
        for j in range(len(matrix[0]) - 1):
            temp[i].append(matrix[i][j])
    return temp


def finding_two_leaves(matrix, node):
    length = len(matrix)
    for i in range(length):
        for k in range(length):
            if i != node and k != node:
                if matrix[i][k] == matrix[i][node] + matrix[k][node]:
                    return i, k


if __name__ == '__main__':
    main()
