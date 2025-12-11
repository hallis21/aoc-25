test = [x.strip() for x in open("test").readlines()]
real = [x.strip() for x in open("real").readlines()]



# start from start and find all paths to end
# no cycles
def bfs(graph, start, end):
    queue = [(start, [start])]
    paths = []

    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == end:
                paths.append(path + [next])
            elif next == "out":
                # if next is "out" then we hit a dead end
                continue
            else:
                

                queue.append((next, path + [next]))
    return paths

def filter_paths(paths, condition):
    return [p for p in paths if condition(p)]


def p1(data):
    nodes = {}
    for line in data:
        source, dests = line.split(":")
        dest_arr = dests.strip().split(" ")

        # nodes += (source, set(dest_arr))
        nodes[source] = set(dest_arr)

    paths = bfs(nodes, "you", "out")
    print("Total paths:", len(paths))
    # must visit fft and dac, any order
    # paths = filter_paths(paths, lambda p: "fft" in p and "dac" in p)
    return len(paths)




# def count_through(nodes, start, c1, c2, end):
#     start_to_c1 = bfs(nodes, start, c1)
#     c1_to_c2 = bfs(nodes, c1, c2)
#     c2_to_end = bfs(nodes, c2, end)

#     count = 0
#     for p1 in start_to_c1:
#           for p2 in c1_to_c2:
#               # overlap, remove required overlap
#               if set(p1[:-1]) & set(p2[1:]):  # overlap check
#                   continue
#               for p3 in c2_to_end:
#                 # same overlap
#                   if set(p1[:-1]) & set(p3[1:]) or set(p2[:-1]) & set(p3[1:]):
#                       continue
#                   count += 1
#     return count
    

# def p2(data):
#     nodes = {}
#     for line in data:
#         source, dests = line.split(":")
#         dest_arr = dests.strip().split(" ")

#         # nodes += (source, set(dest_arr))
#         nodes[source] = set(dest_arr)

#     one_paths = count_through(nodes, "svr", "fft", "dac", "out")
#     two_paths = count_through(nodes, "svr", "dac", "fft", "out")
#     return one_paths + two_paths


from functools import lru_cache

# somehow "memoized DFS with bitmask"
# googled to this, makes sense, not my idea

# did not work still

def p2(data):
    nodes = {}
    for line in data:
        source, dests = line.split(":")
        dest_arr = dests.strip().split(" ")
        nodes[source] = set(dest_arr)

    # Collect ALL node names (sources + destinations)
    all_nodes = set(nodes.keys())
    for dests in nodes.values():
        all_nodes.update(dests)
    all_nodes = list(all_nodes)
    idx = {n: i for i, n in enumerate(all_nodes)}

    must_mask = (1 << idx["fft"]) | (1 << idx["dac"])

    @lru_cache(maxsize=None)
    def dfs(node, visited):
        if node == "out":
            return 1 if (visited & must_mask) == must_mask else 0

        count = 0
        for neighbor in nodes[node]:
            bit = 1 << idx[neighbor]
            if not (visited & bit):
                count += dfs(neighbor, visited | bit)
        return count

    return dfs("svr", 1 << idx["svr"])


from collections import defaultdict, deque
# Inclusion-Exclusion
# also not my idea
# this beast
# |A ∩ B| = |All| - |not A| - |not B| + |not A and not B|
#
# big issue with previous was that this is an acyclic dag
# no cycles makes counting paths easier with dp
def count_paths_dag(graph, start, end, exclude=set()):
      # Build filtered adjacency + reverse graph
      adj = defaultdict(list)
      in_degree = defaultdict(int)
      all_nodes = set()

      for src, dests in graph.items():
          if src in exclude:
              continue
          all_nodes.add(src)
          for dst in dests:
              if dst in exclude:
                  continue
              all_nodes.add(dst)
              adj[src].append(dst)
              in_degree[dst] += 1

      if start not in in_degree:
          in_degree[start] = 0

      # kahn's algorithm
      topo = []
      queue = deque([n for n in all_nodes if in_degree[n] == 0])
      while queue:
          node = queue.popleft()
          topo.append(node)
          for neighbor in adj[node]:
              in_degree[neighbor] -= 1
              if in_degree[neighbor] == 0:
                  queue.append(neighbor)

      # DP: count paths from start to each node
      path_count = defaultdict(int)
      path_count[start] = 1

      for node in topo:
          for neighbor in adj[node]:
              path_count[neighbor] += path_count[node]

      return path_count[end]

def p2(data):
      nodes = {}
      for line in data:
          source, dests = line.split(":")
          nodes[source] = set(dests.strip().split(" "))

      all_paths = count_paths_dag(nodes, "svr", "out")
      no_fft = count_paths_dag(nodes, "svr", "out", {"fft"})
      no_dac = count_paths_dag(nodes, "svr", "out", {"dac"})
      no_both = count_paths_dag(nodes, "svr", "out", {"fft", "dac"})

      return all_paths - no_fft - no_dac + no_both
   




# print("Real:", p1(real))
print("Test:", p2(real))
