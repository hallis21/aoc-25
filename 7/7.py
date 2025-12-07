test = [x.strip() for x in open("test").readlines()]
real = [x.strip() for x in open("real").readlines()]


def print_board(data, beams):
    board = [list(x) for x in data]
    for beam in beams:
        x, y = beam
        board[y][x] = "|"
    for line in board:
        print("".join(line))
    print()

def p1(data):

    beams = set() # list of x,y
    splitters = [] # list of x,y

    # find first "S" and add coordinates to beams
    # in first line
    beams.add( (data[0].index("S"), 0) )
    all_beams = set()
    all_beams.add( (data[0].index("S"), 0) )

    for line in range(len(data)):
        for char in range(len(data[line])):
            if data[line][char] == "^":
                splitters.append( (char, line) )
   

    n_splits = 0
    idx = 0
    for level in range(len(data)):
        new_beams = set()
        for beam in beams:
            x, y = beam
            
            if y+1 < len(data):
                below = data[y+1][x]
                if below == ".":
                    new_beams.add( (x, y+1) )
                elif below == "^":
                    # find splitter
                    new_beams.add( (x-1, y+1) )
                    new_beams.add( (x+1, y+1) )
                    n_splits += 1
                    
        all_beams.update(new_beams)
        beams = new_beams
        idx += 1

    return n_splits





def p2(data):
    beams = list() # list of x,y
    splitters = [] # list of x,y

    # find first "S" and add coordinates to beams
    # in first line
    beams.append( (data[0].index("S"), 0) )
    all_beams = set()
    all_beams.add( (data[0].index("S"), 0) )

    for line in range(len(data)):
        for char in range(len(data[line])):
            if data[line][char] == "^":
                splitters.append( (char, line) )    

    n_splits = 0
    idx = 0
    for level in range(len(data)-1):
        print(level, len(beams))
        new_beams = list()
        for beam in beams:
            x, y = beam
            
            if y+1 < len(data):
                below = data[y+1][x]
                if below == ".":
                    new_beams.append( (x, y+1) )
                elif below == "^":
                    # find splitter
                    new_beams.append( (x-1, y+1) )
                    new_beams.append( (x+1, y+1) )
                    n_splits += 1
                    
        all_beams.update(new_beams)
        beams = new_beams
        idx += 1

    # counter beams at the last line

    return len(beams)


def p2_v2(data):
    # find all splitters and memoize beam counts bottom-up
    splitters = {}  # (x, y) 

    for y in range(len(data) - 1, -1, -1):
        for x, ch in enumerate(data[y]):
            if ch == '^':
                # left
                left_count = trace_beam(data, x - 1, y, splitters)
                # right
                right_count = trace_beam(data, x + 1, y, splitters)
                splitters[(x, y)] = left_count + right_count

    # for y in range(len(data)):
    #     row = []
    #     for x in range(len(data[y])):
    #         if (x, y) in splitters:
    #             row.append(splitters[(x, y)])
    #         else:
    #             row.append(data[y][x])
    #     print(row)

    # Now trace from start position
    start_x = data[0].index("S")
    return trace_beam(data, start_x, 0, splitters)


def trace_beam(data, x, y, splitters):
    # follow a single beam down until split or wexit
    while y + 1 < len(data):
        y += 1
        ch = data[y][x]
        if ch == '^':
            return splitters[(x, y)]
    return 1




# print("Test:", p1(real))

# print("Real:", p2(real))
print("Real:", p2_v2(real))
