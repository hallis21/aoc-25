test = [x for x in open("test").readlines()]
real = [x for x in open("real").readlines()]




def p1(data):
   
    # Read lines until and turn into ints
    # last line contains chars

    nums = []
    for line in data:
        #if not numeric
       nums.append(line.split())


    # transpose the nums
    nums = list(zip(*nums))
    res = 0

    # turn first n-1 into ints
    for i in range(len(nums)):
        nums[i] = [int(x) for x in nums[i][:-1]] + [nums[i][-1]]

    for num in nums:
        if num[-1] == "*":
            # multiply all the numbers
            prod = num[0]
            for n in num[1:-1]:
                prod *= n
            res += prod
        elif num[-1] == "+":
            res += sum(num[:-1])


    return   res    
            


    # return   res  



def find_all_chars_in_pos(lines, pos):
    # given an idx pos, find all chars in that pos throughout the lines
    chars = []
    for line in lines:
        chars.append(line[pos])
    return chars

def p2(data):

    nums = ["" for _ in range(len(data[-1].split()))]



    num_rows = []

    cur_sign = ""
    num_idx = 0
    for idx in range(len(data[-1])):
        chars = find_all_chars_in_pos(data, idx)
        
        if all(c == " " for c in chars):
            continue
        if chars[-1] in ["*", "+"]:
            cur_sign = chars[-1]
            num_idx += 1
        num_rows.append((int("".join(chars[:-1]).strip()), cur_sign, num_idx - 1))


    # calculate the result, 
    res = 0
    for nidx in range(num_idx):
        cur_nums = [num for num, sign, idx in num_rows if idx == nidx]
        cur_sign = [sign for num, sign, idx in num_rows if idx == nidx][0]
        if cur_sign == "*":
            prod = 1
            for n in cur_nums:
                prod *= n
            res += prod
        elif cur_sign == "+":
            res += sum(cur_nums)



    return res






# print("Test:", p1(real))

print("Real:", p2(real))
