real = [x.strip().split(",") for x in open("real").readlines()]
test = [x.strip().split(",") for x in open("test").readlines()]

# convert to x,y coords as ints
real = [(int(x), int(y)) for x, y in real]
test = [(int(x), int(y)) for x, y in test]

def to_rect(coord1, coord2):
    # get total area of rectangle defined by coord1 and coord2 (inclusive)
    x1, y1 = coord1
    x2, y2 = coord2
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height

def p1(data):
    # find the biggest rectangle defined by any two coords in data
    recs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            recs.append(to_rect(data[i], data[j]))
    return max(recs)

def print_board(board):
    for row in board:
        print("".join(row))


# Given a position (x, y) on the board, get the next cell at either +/- in x (until hitting a #) or +/- in y (until hitting a #)
# if no hit then return None
def get_next_cells(x, y, coords):
   
    max_y = max(y for x, y in coords)+1
    max_x = max(x for x, y in coords)+1

    next_cells = []

    # check +x
    for nx in range(x + 1, max_x):
        if (nx, y) in coords:
            next_cells.append((nx, y))
            break
    # check -x
    for nx in range(x - 1, -1, -1):
        if (nx, y) in coords:
            next_cells.append((nx, y))
            break
    # check +y
    for ny in range(y + 1, max_y):
        if (x, ny) in coords:
            next_cells.append((x, ny))
            break
    # check -y
    for ny in range(y - 1, -1, -1):
        if (x, ny) in coords:
            next_cells.append((x, ny))
            break
    return next_cells


def point_in_polygon(x, y, polygon):
      """polygon is a list of (x, y) vertices"""
      n = len(polygon)
      inside = False

      j = n - 1
      for i in range(n):
          xi, yi = polygon[i]
          xj, yj = polygon[j]

          if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
              inside = not inside
          j = i

      return inside




def p2(data):
    # Make the board, each coord is #
    max_x = max(x for x, y in data)+1
    max_y = max(y for x, y in data)+1
    board = None
    if len(data) < 100:
        board = [["." for _ in range(max_x)] for _ in range(max_y)]
        for x, y in data:
            board[y][x] = "#"
    # print the board
    # print_board(board)

    set_of_coords = set(data)
    set_filled = set()

    # For each coord, find the next cells in each direction
    
    for x, y in data:
        next_cells = get_next_cells(x, y, set_of_coords)
        # "fill" the space between the coord and the next cells
        for nx, ny in next_cells:
            if nx == x:
                # vertical fill
                for fy in range(min(y, ny) + 1, max(y, ny)):
                    set_filled.add((x, fy))
                    if board: board[fy][x] = "X"
            elif ny == y:
                # horizontal fill
                for fx in range(min(x, nx) + 1, max(x, nx)):
                    set_filled.add((fx, y))
                    if board: board[y][fx] = "X"

    

    if board: print_board(board)

    full_shape = set_of_coords.union(set_filled)

    # make a ranked list of all the biggest rectangles that can be made from the original coords
    rectangles = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            rect_area = to_rect(data[i], data[j])
            rectangles.append((rect_area, data[i], data[j]))
    rectangles.sort(reverse=True, key=lambda x: x[0])

    print("Total filled:", len(rectangles))
    if board:
        for rect in rectangles:
            print(rect)


    # start from the biggest rectangle, see if each wall piece is inside the shape
    i = 0
    for rect_area, coord1, coord2 in rectangles[:]:
        i += 1
        if i % 100 == 0 or len(data) < 100:
            print(f"Checking rectangle {i}/{len(rectangles)}: {coord1} -> {coord2}, area={rect_area}")
        x1, y1 = coord1
        x2, y2 = coord2

        # get the 4 corners of the rectangle
        corners = [
            (min(x1, x2), min(y1, y2)),
            (min(x1, x2), max(y1, y2)),
            (max(x1, x2), min(y1, y2)),
            (max(x1, x2), max(y1, y2)),
        ]

        # check if all 4 corners are in the full shape
        # inside counts so we must use point_in_polygon if not in full_shape
        all_corners_in_shape = True
        for cx, cy in corners:
            if (cx, cy) not in full_shape:
                # Use 'data' which has vertices in order, not full_shape
                if not point_in_polygon(cx, cy, data):
                    all_corners_in_shape = False
                    break
                
        # If this is the case then we must check if ALL the edge points are in the shape
        # meaning the full walls of the rectangle
        walls = []
        for x in range(min(x1, x2), max(x1, x2) + 1):
            walls.append((x, min(y1, y2)))
            walls.append((x, max(y1, y2)))
        for y in range(min(y1, y2), max(y1, y2) + 1):
            walls.append((min(x1, x2), y))
            walls.append((max(x1, x2), y))

        for wx, wy in walls:
            if (wx, wy) not in full_shape:
                if not point_in_polygon(wx, wy, data):
                    all_corners_in_shape = False
                    break

        if all_corners_in_shape:
            return rect_area
    


# print("P1:", p1(real))
print("P2:", p2(test))
# print("Real:", p2_v2(real))
