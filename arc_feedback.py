'''
Exact and approximate feedback arc set computation for directed graphs.
'''

import itertools, toposort

def approx_ranking(graph):
    '''
    Compute an approximate ranking for the given graph (based on percentage system)
    '''
    # Round Robin algorithm
    # Count percentage of "matchups" that each project wins
    res = {}
    for i in graph.keys():
        res[i]['wins'] = 0
        res[i]['losses'] = 0
    for i in graph:
        for j in graph[i]:
            res[i]['wins'] += 1
            res[j]['losses'] += 1
    for project in res:
        res[project]['percent'] = res[project]['wins'] / (res[project]['wins'] + res[project]['losses'])
    
    # Sort by percentage
    res = sorted(res.items(), key=lambda x: -x[1]['percent'])

    # Print result
    for project in res:
        print(f"{project[0]} -> Wins: {project[1]["wins"]}, Losses: {project[1]["losses"]}, Percent: {project[1]["percent"]:.2f}")

    return res

def exact_fas(graph):
    '''
    Compute the exact feedback arc set for the given graph
    '''