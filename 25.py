from random import randrange


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def remove_edge(vertices, edges, e):
    u, v = e
    edges = list(filter(lambda edge: edge != e and edge != (v, u), edges))
    vertices.remove(u)
    vertices.remove(v)
    uv = f"{u}{v}"
    vertices.append(uv)
    to_remove = []
    to_add = []
    for edge in edges:
        a, b = edge
        if a == u or a == v:
            to_remove.append(edge)
            to_add.append((uv, b))
        if b == u or b == v:
            to_remove.append(edge)
            to_add.append((a, uv))
    for a in to_remove:
        edges.remove(a)
    for a in to_add:
        edges.append(a)
    return vertices, edges


def contract(vertices, edges):
    while len(vertices) > 2:
        idx = randrange(len(edges) // 2)
        e = edges[idx]
        vertices, edges = remove_edge(vertices, edges, e)
    return vertices, edges


def part1(input):
    vertices = []
    edges = []
    for line in input:
        f, t = line.split(":")
        tl = t.split()
        if f not in vertices:
            vertices.append(f)
        for c in tl:
            if c not in vertices:
                vertices.append(c)
            edges.append((f, c))

    cut_e = edges
    while len(cut_e) != 3:
        cut_v, cut_e = contract(vertices.copy(), edges.copy())
        print("CUT-E", len(cut_e))

    v1, v2 = cut_v
    return len(v1) // 3 * len(v2) // 3


testInput = readInput("25_test.txt")
assert part1(testInput) == 54

input = readInput("25.txt")
print(part1(input))
