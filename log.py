'''
Logging utilities
'''

import builtins, os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(THIS_FOLDER, 'log.txt')

def print(*args, important=False, **kwargs):
    '''
    Print to stdout while also logging to file.
    '''
    builtins.print("\n" if important else "  * ", end="")
    builtins.print(*args, **kwargs)
    with open(log_file, "a") as f:
        builtins.print("\n" if important else "  * ", end="", file=f)
        builtins.print(*args, file=f, **kwargs)