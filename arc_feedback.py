'''
Exact and approximate feedback arc set computation for directed graphs.
'''

import itertools, toposort
from log import print

def powerset(iterable):
    '''
    Compute the powerset of the given iterable
    '''
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )

def approx_ranking(graph):
    '''
    Compute an approximate ranking for the given graph (based on percentage system)
    '''
    # Round Robin algorithm
    # Count percentage of "matchups" that each project wins
    res = {}
    for i in graph.keys():
        res[i] = {}
        res[i]['wins'] = 0
        res[i]['losses'] = 0
    for i in graph.keys():
        for j in graph[i]:
            res[i]['wins'] += 1
            res[j]['losses'] += 1
    for project in res:
        res[project]['percent'] = res[project]['wins'] / (res[project]['wins'] + res[project]['losses'])
    
    # Sort by percentage
    res = sorted(res.items(), key=lambda x: -x[1]['percent'])

    # Print result
    for project in res:
        print(f'{project[0]} -> Wins: {project[1]["wins"]}, Losses: {project[1]["losses"]}, Percent: {project[1]["percent"]:.2f}')

    return res

def exact_fas(graph):
    '''
    Compute the exact feedback arc set for the given graph
    '''
    # Select top 5 projects and compute edge weights
    # Weight = number of times project is ranked higher than another project
    g = []

    min_loss = float("inf")

    # Iterate through all possible subsets of arcs
    edges = []
    for i in graph:
        for j in graph[i].keys():
            edges.append((i, j, graph[i][j]))
    for subset in powerset(edges):
        # Check if subset is a feedback arc set
        toposorting = is_fas(subset, graph)
        if toposorting:
            # Check if subset is a minimal feedback arc set
            subset_sum = sum([edge[2] for edge in subset])
            if subset_sum < min_loss:
                min_loss = subset_sum
                g = []
            if subset_sum == min_loss:
                g.append(toposorting)
    
    return g[0][::-1]

def is_fas(subset, graph):
    '''
    Check if the given subset of edges is a feedback arc set
    '''
    # Compute graph with subset of edges removed
    g = {}
    for i in graph:
        g[i] = {}
        for j in graph[i]:
            g[i][j] = graph[i][j]
    for edge in subset:
        g[edge[0]].pop(edge[1])
    # Check if graph is acyclic, if so return a topological sort
    return toposort.toposort(g)