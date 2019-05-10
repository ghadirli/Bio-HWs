def main():
    text = input()
    print(suffix_array(text))

    patterns = input().split()
    d = int(input())
    # index = multiple_approximate_pattern_matching(text, patterns, d)


def multiple_approximate_pattern_matching(text, patterns, d):
    bwt = burrows_wheeler_transform(text)
    arr = suffix_array(text)
    last = [bwt[i] for i in range(len(bwt))]
    first = [CharNode(text[i], i) for i in range(len(last))]
    first.sort()
    

def suffix_array(string):
    suffixes = []
    for i in range(len(string)):
        suffixes.append(string[i: len(string)])
    suffixes.sort()
    suffixes = [len(string) - len(s) for s in suffixes]
    return suffixes


def burrows_wheeler_transform(text):
    suffix = []
    current_text = text
    for i in range(len(text)):
        suffix.append(current_text)
        current_text = current_text[-1] + current_text[0:len(current_text) - 1]
    suffix.sort()
    return ''.join([s[-1] for s in suffix])


class CharNode:
    def __init__(self, s, i):
        self.symbol = s
        self.index = i

    def __eq__(self, other):
        return self.symbol - other.symbol


if __name__ == '__main__':
    main()
