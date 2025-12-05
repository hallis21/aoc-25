test = [x.strip() for x in open("test").readlines()]
real = [x.strip() for x in open("real").readlines()]




def p1(data):
   
    # Read lines until blank line
    res = 0

    # format (start, bool (start or end))
    nums = []

    line_index = 0
    for line in data:        
        line_index += 1
        if line == "":
            break
        parts = line.split("-")
        start = int(parts[0])
        end = int(parts[1])
        nums.append((start, True))  # True for start
        nums.append((end, False))    # False for end
        
    # Insert all the nums from the next lines
    for line in data[line_index:]:
        num = int(line.strip())
        nums.append((num, None)) # since real nul

    # sort the nums by the first element, prioritize true, then none, then false
    nums.sort(key=lambda x: (x[0], x[1] is False, x[1] is None))


    cur_active = 0 # count how many trues vs falses we have currently
    for num in nums:
        print("Processing:", num)
        if num[1] is True:  # start
            cur_active += 1
        elif num[1] is None:  # end
            if cur_active > 0:
                res += 1
                print("Adding:", num[0])
        else:  # just a number
            cur_active -= 1
    


    print("nums:", nums)



    return   res  


def p2(data):
   
    # Read lines until blank line
    res = 0

    # format (start, bool (start or end))
    nums = []

    line_index = 0
    for line in data:        
        line_index += 1
        if line == "":
            break
        parts = line.split("-")
        start = int(parts[0])
        end = int(parts[1])
        nums.append((start, True)) 
        nums.append((end, False))   
        

    nums.sort(key=lambda x: (x[0], x[1] is False, x[1] is None))

    # find all the new ranges (where we have a start, and all the way until no actives)
    ranges = []
    cur_active = 0  # count how many trues vs falses we have currently
    cur_range = None
    for num in nums:
        # print("Processing:", num)
        if num[1] is True:  # start
            cur_active += 1
            if cur_range is None:
                cur_range = [num[0], None]  # start a new range
        elif num[1] is False:  # end
            cur_active -= 1
            if cur_active == 0 and cur_range is not None:
                cur_range[1] = num[0]  
                ranges.append(cur_range)  
                cur_range = None  
        else: 
            pass

    for r in ranges:
        if r[1] is not None:  # if we have a valid range
            res += (r[1] - r[0] + 1)  # count the numbers in the range

    print("Ranges:", ranges)
    return res        

# print("Test:", p1(real))

print("Real:", p2(real))
