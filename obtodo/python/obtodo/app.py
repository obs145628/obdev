'''
Usage:

obtodo: <project-path>

Go through all files, and look for lines that contain a certain pattern,
to target it as a TODO instruction.

They are different todo levels

- Isue: Really important and prioritary task to do (bug, primary feature)
  tags: @ bug / @ issue / @ main

- Todo: Task that is required to finish the project
  tags: @ todo / @ task

- Optional: Task that would be good to do, but the project can be finished without it.
  Usually it's because implem is too slow, or some edge cares are not handled
  tags: @ extra / @ optional

- Feature: A missing interesting feature, that I am not planning to add for now
  tags: @ feature

- Idea: Some random ideas about what other things I could do
  tags: @ idea

- Info: Any kind of remarks, details worth noticing.
  tags: @ info / @ tip

The lower the level, the more important it is.
It's possible to filter tasks to display only those <= specific level

It looks for tag on comment lines, usually it's uppercase but search is case insensitive

A todo can have extra properties using eg @ todo:desc
Usually desc is one work, like a project name, to filter by project


'''

import os
import sys

from pyutils.filesfinder import FilesFinder, FilterType
from pyutils import projects_list

from .todoitem import TodoItem, TAGS_LEVELS, TAGS_SYM

IGNORE_DIRS = ['_build', 'extern']
TXT_EXTS=['.txt', '.c', '.cc', '.h', '.hh', '.md', '.MD', '.py']

MIN_TAG = min(TAGS_LEVELS.values())
MAX_TAG = max(TAGS_LEVELS.values())

def filter_tags(max_level):
    return { key: TAGS_LEVELS[key] for key in TAGS_LEVELS if TAGS_LEVELS[key] <= max_level }

def parse_file(path, rel_path, res, dir_label, max_level):
    with open(path, 'r') as f:
        lines = []
        try:
            lines = f.readlines()
        except:
            pass
        
        for (l_idx, l) in enumerate(lines):
            l = l.strip()
            ll = l.lower()
            tags = list(filter_tags(max_level).keys())
            for t in tags:
                if t in ll:
                    res.append(TodoItem(path, rel_path, dir_label, l_idx + 1, l))
                    break


'''
Go through all files in dir `dir_path`
Only keep tasks of level `max_level` or less
Retturns list<TodoItem>
Give a more readable path than `dir_path` when pritting tasks
'''
def find_tasks(dir_path, dir_label = None, max_level = 1000):
    if not os.path.isdir(dir_path):
        raise Exception('{} not a dir'.format(dir_path))
    ff = FilesFinder()
    ff.filter_ext_is_any(TXT_EXTS, FilterType.File)
    ff.filter(lambda x, _: os.path.basename(x) not in IGNORE_DIRS, FilterType.Rec)
    files, _ = ff.run(dir_path)

    res = list()
    for f in files:
        parse_file(f, os.path.relpath(f, dir_path), res, dir_label, max_level)
    return res

'''
`tasks` list<TodoItem>
dump them all to `os` stream, by level
'''
def dump_tasks(tasks, os):
    for level in range(MIN_TAG, MAX_TAG+1):
        tt = [t for t in tasks if t.ty == level]
        if len(tt) == 0:
            continue

        for t in tt:
            os.write('{}\n'.format(t))
        os.write('\n')
    os.flush()

def main(args):
    if len(args) < 1:
        sys.stderr.write('obtodo: Missing <project-path> argument\n')
        return 1

    dir_path = args[0]
    full_path = projects_list.resolve_dirname(dir_path)
    tasks = find_tasks(full_path, dir_label=None, max_level=1000)
    dump_tasks(tasks, sys.stdout)
    return 0
    
    
    

