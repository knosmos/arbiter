'''
Simple topological sort implementation.
'''

def toposort(data):
    # First pass: build a dict mapping each item to a set of its
    # dependencies, and a set of all items with no known dependencies.
    deps = {}
    no_deps = set()
    for item, dep_list in data.items():
        if not dep_list:
            no_deps.add(item)
        else:
            deps[item] = set(dep_list)

    # Second pass: repeatedly find an item with no dependencies, remove it
    # from the deps dict, and add it to the result.
    result = []
    while no_deps:
        item = no_deps.pop()
        result.append(item)
        for dep, dep_list in list(deps.items()):
            dep_list.discard(item)
            if not dep_list:
                no_deps.add(dep)
                del deps[dep]

    if deps:
        raise ValueError('Cyclic dependencies exist among these items: {}'
                         .format(', '.join(repr(x) for x in deps)))
    return result