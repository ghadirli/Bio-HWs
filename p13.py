_end = "_end_"
root = 0


def main():
    text = input()
    patterns = []
    while True:
        s = input()
        if s == "end":
            break
        patterns.append(s)
    trie = make_trie(patterns)
    index = trie_matching(text, trie)
    for i in range(len(index)):
        print(index[i], end=" ")


def prefix_trie_matching(text, trie):
    index = 0
    symbol = text[index]
    v = root
    while True:
        if len(trie[v]) == 0:
            return True
        elif symbol in trie[v]:
            v = trie[v][symbol]

            index += 1
            if index != len(text):
                symbol = text[index]
            else:
                if len(trie[v]) == 0:
                    return True
                else:
                    return False
        else:
            return False


def trie_matching(text, trie):
    index = []
    length = len(text)
    while len(text) != 0:
        if prefix_trie_matching(text, trie):
            index.append(length - len(text))
        text = text[1:]
    return index


def make_trie(patterns):
    trie = {root: {}}
    trie_len = 1
    for pattern in patterns:
        current_node = root
        for i in range(len(pattern)):
            current_symbol = pattern[i]
            if current_symbol in trie[current_node]:
                current_node = trie[current_node][current_symbol]
            else:
                trie[trie_len] = {}
                trie[current_node][current_symbol] = trie_len
                current_node = trie_len
                trie_len += 1

    return trie


if __name__ == '__main__':
    main()
