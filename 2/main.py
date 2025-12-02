test = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
real = open("inp").read()
def p1():
    inp =  [[int(y) for y in x.split("-")] for x in test.split(",")]
    rngs = [[z for z in [str(y) for y in range(x[0], x[1]+1)] if not (len(z) % 2)] for x in inp]
    dbs = []

    s = 0

    # flatten
    for n in [item for sublist in rngs for item in sublist]:
        if n[:len(n)//2] == n[len(n)//2:]:
            s += int(n)

    print(s)


def p2():
    inp =  [[int(y) for y in x.split("-")] for x in real.split(",")]
    rngs = [[z for z in [str(y) for y in range(x[0], x[1]+1)]] for x in inp]
    dbs = []

    for n in  [item for sublist in rngs for item in sublist]:
        for ss in range(len(n)//2):
            nn = n[:ss+1]
            c = n.count(nn)
            if len(nn) * c ==len(n):
                dbs.append(n)
                print("hey ", n)
                break
     # flatten
    s  = 0
   
    print(sum([int(x) for x in dbs]))

def main():
    p2()


if __name__ == "__main__":
    main()
