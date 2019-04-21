from math import inf
from Bio.SubsMat import MatrixInfo as blo

blosum = blo.blosum62

penalty = 5


def linear_space_alignment(left, right, top, bottom, v, w):
    if left == right:
        result = []
        for i in range(top, bottom + 1):
            result.append((i, left))
        return result
    if top == bottom:
        result = []
        for i in range(left, right + 1):
            result.append((top, i))
        return result
    mid = middle_node(left, right, top, bottom, v, w)
    before_mid_node = linear_space_alignment(left, mid[1], top, mid[0], v, w)
    after_mid_node = linear_space_alignment(mid[3], right, mid[2], bottom, v, w)
    return before_mid_node + after_mid_node


def score_alignment(alignment, v, w):
    score = 0
    for i in range(len(alignment) - 1):
        if alignment[i][0] == alignment[i + 1][0] or alignment[i][1] == alignment[i + 1][1]:
            score -= penalty
        else:
            key = (v[alignment[i][1]], w[alignment[i][0]])
            if key not in blosum:
                key = tuple(reversed(key))
            score += blosum[key]
    return score


def get_path(alignment, v, w):
    v_after = ""
    w_after = ""
    for i in range(len(alignment) - 1):
        if alignment[i][1] == alignment[i + 1][1]:
            v_after += "-"
            w_after += w[alignment[i][0]]
        elif alignment[i][0] == alignment[i + 1][0]:
            w_after += "-"
            v_after += v[alignment[i][1]]
        else:
            w_after += w[alignment[i][0]]
            v_after += v[alignment[i][1]]
    return v_after, w_after


def middle_node(left, right, top, bottom, v, w):
    mid_col = int((left + right) / 2)
    length = bottom - top + 1
    score_before = []
    for i in range(length):
        score_before.append(-inf)

    score_after = [0]
    for i in range(length):
        score_after.append(-inf)

    for j in range(left, mid_col + 1):
        for i in range(top, bottom + 1):
            if j != left:
                score_after[i - top] = max(score_before[i - top] - penalty, score_after[i - top])

            if i != top:
                score_after[i - top] = max(score_after[i - top], score_after[i - 1 - top] - penalty)
                if j > left:
                    key = (v[j - 1], w[i - 1])
                    if key not in blosum:
                        key = tuple(reversed(key))
                    score_after[i - top] = max(score_after[i - top], score_before[i - 1 - top] + blosum[key])

        if j < mid_col:
            score_before = []
            for i in score_after:
                score_before.append(i)
            score_after = [-inf] * len(score_after)

    score_before = []
    scores = score_after.copy()

    for i in range(length):
        score_before.append(-inf)

    score_after = []
    for i in range(length):
        score_after.append(-inf)
    score_after[length - 1] = 0

    for j in range(right, mid_col - 1, -1):
        for i in range(bottom, top - 1, -1):
            if i != bottom:
                score_after[i - top] = max(score_after[i - top], score_after[i + 1 - top] - penalty)
                if j < right:
                    key = (v[j], w[i])
                    if key not in blosum:
                        key = tuple(reversed(key))
                    score_after[i - top] = max(score_after[i - top], score_before[i + 1 - top] + blosum[key])
            if j != right:
                score_after[i - top] = max(score_after[i - top], score_before[i - top] - penalty)
        if j != mid_col:
            score_before = []
            for i in score_after:
                score_before.append(i)
            score_after = [-inf] * len(score_after)
    temp = [0] * len(score_after)
    for i in range(len(score_after)):
        temp[i] = scores[i] + score_after[i]
    scores = temp
    mid_row = scores.index(max(scores)) + top

    if score_after[mid_row - top] + penalty == score_before[mid_row - top]:
        return mid_row, mid_col, mid_row, mid_col + 1
    elif score_after[mid_row - top] + penalty == score_after[mid_row + 1 - top]:
        return mid_row, mid_col, mid_row + 1, mid_col
    else:
        return mid_row, mid_col, mid_row + 1, mid_col + 1


def main():
    v = input()
    w = input()
    m = len(v)
    n = len(w)

    alignment = linear_space_alignment(0, m, 0, n, v, w)
    print(score_alignment(alignment, v, w))
    path = get_path(alignment, v, w)
    print(path[0])
    print(path[1])


if __name__ == '__main__':
    main()
