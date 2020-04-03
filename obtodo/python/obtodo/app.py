'''
Usage:

obtodo: <project-path>

Go through all files, and look for lines that contain a certain pattern,
to target it as a TODO instruction.

They are different todo levels

- Isue: Really important and prioritary task to do (bug, primary feature)
  tags: @bug / @issue / @main

- Todo: Task that is required to finish the project
  tags: @todo / @task

- Optional: Task that would be good to do, but the project can be finished without it.
  Usually it's because implem is too slow, or some edge cares are not handled
  tags: @extra / @optional

- Feature: A missing interesting feature, that I am not planning to add for now
  tags: @feature

- Idea: Some random ideas about what other things I could do
  tags: @idea

- Info: Any kind of remarks, details worth noticing.
  tags: @info / @tip

The lower the level, the more important it is.
It's possible to filter tasks to display only those <= specific level

It looks for tag on comment lines, usually it's uppercase but search is case insensitive


'''

import os
import sys

from pyutils.filesfinder import FilesFinder, FilterType

from .todoitem import TodoItem, TAGS_LEVELS, TAGS_SYM

IGNORE_DIRS = ['_build', 'extern']
TXT_EXTS=['.txt', '.c', '.cc', '.h', '.hh', '.md', '.MD']

MIN_TAG = min(TAGS_LEVELS.values())
MAX_TAG = max(TAGS_LEVELS.values())


def parse_file(path, rel_path, res):
    with open(path, 'r') as f:
        for (l_idx, l) in enumerate(f.readlines()):
            l = l.strip()
            ll = l.lower()
            for t in TAGS_SYM:
                if t in ll:
                    res.append(TodoItem(path, rel_path, l_idx + 1, l))
                    break

def main(args):
    if len(args) < 1:
        sys.stderr.write('obtodo: Missing <project-path> argument\n')
        return 1

    path = args[0]

    ff = FilesFinder()
    ff.filter_ext_is_any(TXT_EXTS, FilterType.File)
    ff.filter(lambda x, _: os.path.basename(x) not in IGNORE_DIRS, FilterType.Rec)
    #ff.filter_begin_with('_build', FilterType.Rec)
    files, _ = ff.run(path)

    res = list()
    for f in files:
        
        parse_file(f, os.path.relpath(f, path), res)


    for level in range(MIN_TAG, MAX_TAG+1):
        tasks = [t for t in res if t.ty == level]
        if len(tasks) == 0:
            continue

        for t in tasks:
            print(t)
        print('')

    return 0
    
    
    

