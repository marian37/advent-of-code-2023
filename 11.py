def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def solution(input, expandedBy):
    lr = len(input)
    lc = len(input[0])
    expandedRows = []
    expandedColumns = []
    galaxies = []
    for r in range(lr):
        if all(map(lambda x: x == ".", input[r])):
            expandedRows.append(r)
    for c in range(lr):
        column = [input[i][c] for i in range(lr)]
        if all(map(lambda x: x == ".", column)):
            expandedColumns.append(c)

    rows = 0
    for r in range(lr):
        cols = 0
        if r in expandedRows:
            rows += expandedBy - 1
            continue
        for c in range(lc):
            if c in expandedColumns:
                cols += expandedBy - 1
            if input[r][c] != ".":
                galaxies.append((r + rows, c + cols))

    result = 0
    for i in range(len(galaxies)):
        gr, gc = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            ngr, ngc = galaxies[j]
            result += abs(ngr - gr) + abs(ngc - gc)

    return result


testInput = readInput("11_test.txt")
assert solution(testInput, 2) == 374
assert solution(testInput, 10) == 1030
assert solution(testInput, 100) == 8410

input = readInput("11.txt")
print(solution(input, 2))
print(solution(input, 1000000))
