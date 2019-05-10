def main():
    bwt = input()
    print(reconstruct_from_bwt(bwt))


def reconstruct_from_bwt(bwt):
    chars = [c for c in bwt]
    chars.sort()
    first_col = ''.join(chars)
    first_col = [(first_col[i], first_col[:i + 1].count(first_col[i])) for i in range(len(first_col))]
    last_col = [(bwt[i], bwt[:i + 1].count(bwt[i])) for i in range(len(bwt))]

    inverse_bwt = [('$', 1)]
    for i in range(1, len(bwt)):
        s = first_col[last_col.index(inverse_bwt[i - 1])]
        inverse_bwt.append(s)
    inverse_bwt = [i[0] for i in inverse_bwt]
    inverse_bwt.append(inverse_bwt[0])
    del inverse_bwt[0]
    return ''.join(inverse_bwt)


if __name__ == '__main__':
    main()
