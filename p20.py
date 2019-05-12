import re

alphabet = ['A', 'T', 'C', 'G']


def main():
    n = int(input())
    nodes = {}
    leaves = {}
    for i in range(n):
        line = input()
        line = re.search("(\d+)->(\w+)", line)
        leaves[i] = line.group(2)
        node = int(line.group(1))
        if node not in nodes:
            nodes[node] = []

        nodes[int(line.group(1))].extend([i])
    while True:
        s = input()
        if s == "end":
            break
        s = re.search("(\d+)->(\d+)", s)
        node = int(s.group(1))
        if node not in nodes:
            nodes[node] = []
        nodes[int(s.group(1))].extend([int(s.group(2))])
    print(nodes)
    print(leaves)
    char_leaves = []
    for j in range(len(leaves[0])):
        ali = {}
        for leave in leaves.keys():
            ali[leave] = {}
            ali[leave] = leaves[leave][j]
        char_leaves.append(ali)
        # print(char_leaves[-1])

    score, res = small_parsimony(nodes, char_leaves[0])
    # result = [small_parsimony(nodes, character) for character in char_leaves]
    # print(res, score)
    # print("strings:")
    # for i in range(len(char_leaves)):
    #     u, v = small_parsimony(nodes, char_leaves[i])
    #     print(u, v)
    u, v = small_parsimony(nodes, char_leaves[3])
    print(u, v)
    result = {}
    final_score = 0
    for i in range(len(char_leaves)):
        score, tree = small_parsimony(nodes, char_leaves[i])
        for key in tree.keys():
            if key not in result:
                result[key] = ""
            result[key] = result[key] + tree[key]
        final_score += score
    whole_tree = list(nodes.keys())
    whole_tree.extend(list(leaves.keys()))
    final_result = []
    for i in whole_tree:
        for j in whole_tree:
            if i != j:
                if (result[i], result[j]) not in final_result:
                    if i in nodes:
                        if j in nodes[i]:
                            final_result.append((result[i], result[j]))

    # print(final_score)
    # for i in range(len(final_result)):
    #     print(final_result[i][0] + "->" + final_result[i][1] + ":" + str(
    #         hamming_distance(final_result[i][0], final_result[i][1])))
    #     print(final_result[i][1] + "->" + final_result[i][0] + ":" + str(
    #         hamming_distance(final_result[i][0], final_result[i][1])))


def hamming_distance(s, t):
    score = 0
    for i in range(len(s)):
        if s[i] != t[i]:
            score += 1
    return score


def small_parsimony(tree, leaves):
    whole_tree = list(tree.keys())
    whole_tree.extend(list(leaves.keys()))
    tag = []
    s = {}
    for i in range(max(tree.keys()) + 1):
        tag.append(0)
    for v in whole_tree:
        tag[v] = 0
        if is_leaf(tree, v):
            tag[v] = 1
            for symbol in alphabet:
                if v not in s:
                    s[v] = {}
                if leaves[v] == symbol:
                    s[v][symbol] = 0
                else:
                    s[v][symbol] = float("inf")
    # print(s)
    ripes = list(tree.keys())
    result = {}
    while len(ripes) > 0:
        v = ripes.pop(0)
        tag[v] = 1
        for symbol in alphabet:
            if v not in s:
                s[v] = {}
            s[v][symbol] = float("inf")
            m1 = float("inf")
            for sym in alphabet:
                daughter = tree[v][0]
                if m1 > s[daughter][sym] + delta(sym, symbol):
                    m1 = s[daughter][sym] + delta(sym, symbol)
            m2 = float("inf")
            for sym in alphabet:
                son = tree[v][1]
                if m2 > s[son][sym] + delta(sym, symbol):
                    m2 = s[son][sym] + delta(sym, symbol)
            s[v][symbol] = m1 + m2
            # result[v] = sym
        result[v] = min(s[v][u] for u in s[v])
        my_char = None
        # for character in s[v]:
        #     if eminem > s[v][character]:
        #         eminem = s[v][character]
        #         my_char = character
        # result[v] = my_char
    result.update(leaves)
    # score = 0
    #
    # for i in whole_tree:
    #     for j in whole_tree:
    #         if i != j and is_neighbour(tree, i, j):
    #             score += hamming_distance(result[i], result[j])
    print(result)
    return min(result[len(whole_tree)+1][alpha] for alpha in alphabet), result


def is_neighbour(tree, i, j):
    if i in tree:
        if j in tree[i]:
            return True
    if j in tree:
        if i in tree[j]:
            return True
    return False


def delta(s1, s2):
    if s1 != s2:
        return 1
    else:
        return 0


def is_leaf(tree, v):
    if v not in tree:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
