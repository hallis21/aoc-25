test = [x.strip() for x in open("test").readlines()]
real = [x.strip() for x in open("real").readlines()]



def get_neighbors(data, x, y, w,h):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield data[ny][nx], nx, ny


def can_be_removed(data, x, y, w=None, h=None):
    # if less than 4 neighbors are filled, it can be removed
    c = data[y][x]
    if c != "@":
        return False
    ns = 0
    for n, _,_ in get_neighbors(data, x, y, w, h):
        if n == "@":
            ns += 1
    return ns < 4

def p1(data):
    res = 0
    w = len(data[0].strip())
    h = len(data)

    for y in range(h):
        for x in range(w):
            c = data[y][x]
            if c == "@":
                ns = 0
                for n, _,_ in get_neighbors(x, y):
                    if n == "@":
                        ns += 1
                if ns < 4:
                    res += 1

    return   res  


def p2(data):
    w = len(data[0].strip())
    h = len(data)
    total_removed = 0

    while True:
        to_remove = []
        for y in range(h):
            for x in range(w):
                if can_be_removed(data, x, y, w, h):
                    to_remove.append((x, y))
        if not to_remove:
            break
        total_removed += len(to_remove)
        for x, y in to_remove:
            data[y] = data[y][:x] + "." + data[y][x+1:]

    return total_removed
   
   


# print("Test:", p1(data))

print("Real:", p2(real))
