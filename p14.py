root = 0


def main():
    text = input()
    patterns = []
    while True:
        s = input()
        if s == "end":
            break
        patterns.append(s)
    # text = text + "$"
    suffix_arr = suffix_array(text)
    print(suffix_arr)
    result = []
    for i in range(len(patterns)):
        result.extend(find_index(text, patterns[i], suffix_arr))
    result.sort()
    for i in range(len(result)):
        print(result[i], end=" ")


def find_index(text, pattern, suffix_arr):
    start = 0
    end = len(text) - 1
    for i in range(len(suffix_arr)):
        if pattern == text[suffix_arr[i]:suffix_arr[i] + len(pattern)]:
            start = i
            break
    for i in range(len(suffix_arr) - 1 - len(pattern), -1, -1):
        if pattern == text[suffix_arr[i]:suffix_arr[i] + len(pattern)]:
            end = i
            break
    return [suffix_arr[i] for i in list(range(start, end + 1))]


#
# def check_prefixabality(text, pattern):
#
# trie[current_node][edge] -> (next_node, edge_symbol, position, label of node(if it's leaf))
def modified_suffix_trie_construction(text):
    trie = {root: {}}
    # first is in  my trie and second is in real trie
    leaf = []
    trie_len = 1
    for i in range(len(text)):
        current_node = root
        for j in range(i, len(text)):
            current_symbol = text[j]
            if current_symbol in [i[0] for i in trie[current_node]]:
                current_node = trie[current_node][current_symbol][0]
            else:
                trie[trie_len] = {}
                trie[current_node][current_symbol] = (trie_len, text.index(current_symbol))
                current_node = trie_len
                trie_len += 1
        if len(trie[current_node]) == 0:
            leaf.append((current_node, i))
    return trie, leaf


def suffix_array(string):
    suffixes = []
    for i in range(len(string)):
        suffixes.append(string[i: len(string)])
    suffixes.sort()
    suffixes = [len(string) - len(s) for s in suffixes]
    return suffixes


def generate_suffixes(text):
    suffixes = []
    for i in range(len(text), -1, -1):
        suffixes.append(text[i: len(text)] + "$")

    return suffixes


if __name__ == '__main__':
    main()
