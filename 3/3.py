test = """987654321111111
811111111111119
234234234234278
818181911112111"""
real = open("inp").read()


def solve(data, num_batteries):
    lines = data.strip().split("\n")
    total = 0

    for line in lines:
        digits = list(line)
        n = len(digits)
        result = []
        start = 0

        # gotta fill the num pos
        for remaining in range(num_batteries, 0, -1):
            # move backwards to find the best digit we can use while keeping order and enough digits left
            best_idx = start
            for i in range(start, n - remaining + 1):
                if digits[i] > digits[best_idx]:
                    best_idx = i
            result.append(digits[best_idx])
            start = best_idx + 1

        joltage = int("".join(result))
        total += joltage

    return total


print("Test:", solve(test, 12))

print("Real:", solve(real, 12))
