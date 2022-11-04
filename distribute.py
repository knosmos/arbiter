'''
Judge project assignment algorithms.
'''

import random, math, itertools
from log import print

def distribute(entries, num_judges, entries_per_judge = 5):
    '''
    Distribute entries into groups.
    '''
    print("Project Distribution ======================", important=True)
    print(f"Number of judges: {num_judges}")
    print(f"Number of entries per judge: {entries_per_judge}")

    rounds = math.ceil(num_judges * entries_per_judge / len(entries))
    
    print(f"Number of rounds: {rounds}")

    connected = False
    repeated = True
    while repeated or not connected:
        print("Generating assignments...")
        entry_list = []
        for i in range(rounds):
            random.shuffle(entries)
            entry_list.extend(entries)
        res = []
        for i in range(num_judges):
            res.append(entry_list[i * entries_per_judge: (i + 1) * entries_per_judge])
        connected = check_connected(res)
        if not connected:
            print("Graph connectivity error, trying again")
        else:
            print("Graph connectivity test passed")
        repeated = False
        for i in res:
            k = [j[0] for j in i]
            if len(set(k)) != len(k):
                repeated = True
        if repeated:
            print("Repeating assignments detected, trying again")
        else:
            print("No repeating assignments found")
    for i in range(len(res)):
        print("Judge", i, ":", ", ".join([k[0] for k in res[i]]))
    return res

def check_connected(assignments):
    '''
    Check if the given assignments are connected.
    '''
    # add edges between projects if they are assigned to the same judge
    # if the resulting graph is connected then the assignments are valid
    
    # build graph
    graph = {}
    for judge in assignments:
        for project1, project2 in itertools.combinations(judge, 2):
            if project1[0] not in graph:
                graph[project1[0]] = set()
            if project2[0] not in graph:
                graph[project2[0]] = set()
            graph[project1[0]].add(project2[0])
            graph[project2[0]].add(project1[0])

    # check connectivity
    # run bfs
    visited = set()
    queue = [list(graph.keys())[0]]
    while len(queue) > 0:
        node = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
    return len(visited) == len(graph)

if __name__ == "__main__":
    # Test distribute
    entries = list("abcdefghijk")
    num_judges = 5
    entries_per_judge = 5
    res = distribute(entries, num_judges, entries_per_judge)
