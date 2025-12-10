real = [x.strip().split(",") for x in open("real").readlines()]
test = [x.strip().split(",") for x in open("test").readlines()]



def read_input(data):
    import re
    line_data = []

    for line in data:
        line = ",".join(line)  # rejoin since it was split on comma

        # Parse lights: [.##.] -> n_lights=4, lit_idxs=[1,2]
        lights_match = re.match(r'\[([.#]+)\]', line)
        lights_str = lights_match.group(1)
        n_lights = len(lights_str)
        target_btn = [True if c == '#' else False for i, c in enumerate(lights_str)]

        # Parse buttons: (3) (1,3) (2) etc - everything between ] and {
        start_idx = line.index("]") + 1
        end_idx = line.index("{")
        buttons_str = line[start_idx:end_idx].strip()

        # Find all parenthesized groups
        buttons = []
        for match in re.finditer(r'\(([^)]+)\)', buttons_str):
            nums = [int(x) for x in match.group(1).split(',')]
            buttons.append(nums)

        # Parse brackets stuff: {3,5,4,7}
        brackets_match = re.search(r'\{([^}]+)\}', line)
        target_jol = [int(x) for x in brackets_match.group(1).split(',')]
        n_joltage = len(target_jol)

        line_data.append((n_lights, target_btn, buttons, n_joltage, target_jol))
    return line_data
        


def press_button(lit_idxs, button):
    for idx in button:
        lit_idxs[idx] = not lit_idxs[idx]
    return lit_idxs

def p1(data):
    data = read_input(data)

    solutions = []


    for i, line in enumerate(data):
        print(f"Processing line {i+1}/{len(data)}")
        n_lights, target_btn, buttons, brackets = line
        # Initialize all lights to off
        lit_idxs = [False] * n_lights
        # cache of states seen and the button presses to get there
        # Store as tuple with state and button presses, as integer
        seen_states = {}
        seen_states[tuple(lit_idxs)] = 0

        # states to explore
        from collections import deque
        queue = deque()
        queue.append((lit_idxs, 0))  # (current state, button presses)

        # For each state, try pressing each button and add the new state to the queue if not seen
        while queue:
            current_state, presses = queue.popleft()
            for button in buttons:
                new_state = press_button(current_state[:], button)
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in seen_states:
                    seen_states[new_state_tuple] = presses + 1
                    queue.append((new_state, presses + 1))
                    # Check if we reached the target
                    if new_state == target_btn:
                        solutions.append(presses + 1)
                        break
            else:
                continue  # only executed if the inner loop did NOT break
            break  # only executed if the inner loop DID break
    
    return sum(solutions)


def press_joltage(joltage, button):
    for idx in button:
        joltage[idx] += 1
    return joltage

def p2(data):
    data = read_input(data)

    solutions = []

    for i, line in enumerate(data):
        print(f"Processing line {i+1}/{len(data)}")

        n_lights, target_btn, buttons, n_joltage, target_jol = line

        # Initialize all joltage to 0
        joltage = [0] * n_joltage

        # cache of states seen and the button presses to get there
        # Store as tuple with state and button presses, as integer
        seen_states = {}
        seen_states[tuple(joltage)] = 0
        # states to explore
        from collections import deque
        queue = deque()
        queue.append((joltage, 0))  # (current state, button presses)

        # For each state, try pressing each button and add the new state to the queue if not seen
        # IF ANY of the joltage values exceed the target (at that index), discard that state
        while queue:
            print(f" Queue size: {len(queue)}")
            current_state, presses = queue.popleft()
            for button in buttons:
                new_state = press_joltage(current_state[:], button)
                new_state_tuple = tuple(new_state)
                if any(new_state[i] > target_jol[i] for i in range(n_joltage)):
                    continue  # discard this state
                if new_state_tuple not in seen_states:
                    seen_states[new_state_tuple] = presses + 1
                    queue.append((new_state, presses + 1))
                    # Check if we reached the target
                    if new_state == target_jol:
                        solutions.append(presses + 1)
                        break
            else:
                continue  # only executed if the inner loop did NOT break
            break  # only executed if the inner loop DID break

    return sum(solutions)

print("P1:", p2(real))
# print("P2:", p2(test))
# print("Real:", p2_v2(real))
