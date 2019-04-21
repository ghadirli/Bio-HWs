def main():
    string = "input"
    print(suffix(string))
    print(prefix(string))
    patterns = []
    while True:
        string = input()
        if string == "exit":
            break
        patterns.append(string)
    for i in range(len(patterns)):
        for j in range(len(patterns)):
            if suffix(patterns[i]) == prefix(patterns[j]):
                print(patterns[i], end=" -> ")
                print(patterns[j])


def suffix(string):
    return string[1:len(string)]


def prefix(string):
    return string[:len(string) - 1]


if __name__ == '__main__':
    main()
