test = [x.strip() for x in open("test").readlines()]
real = [x.strip() for x in open("real").readlines()]


def to_coords(data):
    # xyz, one per line
    coords = set()
    for line in data:
        x, y, z = map(int, line.split(","))
        coords.add((x, y, z))
    return coords

def dist(a, b):
    # straight line euclidean distance
    # i cheated on this one
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5

def find_all_dists(coords):
    dists = {}
    coord_list = list(coords)
    for i in range(len(coord_list)):
        for j in range(i + 1, len(coord_list)):
            a = coord_list[i]
            b = coord_list[j]
            d = dist(a, b)
            dists[(a, b)] = d
    return dists


def p1(data):
    coords = to_coords(data)
    dists = find_all_dists(coords)
    # Make a queue of all (coord1, coord2, dist)
    all_dists = []
    for (a, b), d in dists.items():
        all_dists.append((a, b, d))
    all_dists.sort(key=lambda x: x[2])

    pick_n = 1000

    circuts = []
    coord_to_circut = {}
    # each coord is their own circut to start
    for c in coords:
        circuts.append(set([c]))
        # coord to idx in circuts
        coord_to_circut[c] = len(circuts) - 1


    for a, b, d in all_dists[:pick_n]:
        circut_a_idx = coord_to_circut[a]
        circut_b_idx = coord_to_circut[b]
        if circut_a_idx != circut_b_idx:
            # merge
            circut_a = circuts[circut_a_idx]
            circut_b = circuts[circut_b_idx]
            # update coord to circut mapping
            for c in circut_b:
                coord_to_circut[c] = circut_a_idx
            # merge sets
            circut_a.update(circut_b)
            # remove old circut
            circuts[circut_b_idx] = set()

    # print(circuts)
    # mult the sizes of 3 largest circuts
    r = 0
    sizes = sorted([len(c) for c in circuts], reverse=True)

    # print(sizes)
    r = sizes[0] * sizes[1] * sizes[2]


    return r


def p2(data):
    coords = to_coords(data)
    dists = find_all_dists(coords)
    # Make a queue of all (coord1, coord2, dist)
    all_dists = []
    for (a, b), d in dists.items():
        all_dists.append((a, b, d))
    all_dists.sort(key=lambda x: x[2])

    pick_n = 1000

    circuts = []
    coord_to_circut = {}
    # each coord is their own circut to start
    for c in coords:
        circuts.append(set([c]))
        # coord to idx in circuts
        coord_to_circut[c] = len(circuts) - 1


    active_circuts = len(circuts)

    last_conected_pair = None
    # connect until only 1 circut remains
    for a, b, d in all_dists:
        circut_a_idx = coord_to_circut[a]
        circut_b_idx = coord_to_circut[b]
        if circut_a_idx != circut_b_idx:
            # merge
            circut_a = circuts[circut_a_idx]
            circut_b = circuts[circut_b_idx]
            # update coord to circut mapping
            for c in circut_b:
                coord_to_circut[c] = circut_a_idx
            # merge sets
            circut_a.update(circut_b)
            # remove old circut
            circuts[circut_b_idx] = set()
            # remove from active circuts
            active_circuts -= 1
            last_conected_pair = (a, b, d)


    print("Last connected pair:", last_conected_pair)
    return last_conected_pair[0][0] * last_conected_pair[1][0]


print("P1:", p1(real))
print("P2:", p2(real))
# print("Real:", p2_v2(real))
