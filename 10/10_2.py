from pulp import *

def solve_machine(buttons, targets):
    prob = LpProblem("Joltage", LpMinimize)
    
    # Variables: how many times to press each button
    x = [LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(len(buttons))]
    
    # Objective: minimize total presses
    prob += lpSum(x)
    
    # Constraints: each counter must reach its target
    for counter_idx, target in enumerate(targets):
        prob += lpSum(x[j] for j, btn in enumerate(buttons) if counter_idx in btn) == target
    
    prob.solve(PULP_CBC_CMD(msg=0))
    return int(value(prob.objective))


import re

def parse_line(line):
    buttons = []
    for match in re.findall(r'\(([^)]+)\)', line):
        buttons.append(set(int(x) for x in match.split(',')))
    
    targets_match = re.search(r'\{([^}]+)\}', line)
    targets = [int(x) for x in targets_match.group(1).split(',')]
    
    return buttons, targets

# Example usage
with open('real') as f:
    total = 0
    for line in f:
        buttons, targets = parse_line(line.strip())
        total += solve_machine(buttons, targets)
    print(total)