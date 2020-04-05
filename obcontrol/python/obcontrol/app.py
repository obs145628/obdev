'''
Usage
python control-cli.py <task> ...


# project

`project list`
List all projects with absolute path to main file

# todo

`todo <projname>
Run todo on all repos of a specific project
If no project specified, run on all projects
Print all tasks

@todo be able to print for all projects

'''


import os
import sys
from io import StringIO

from pyutils import projects_list

import obtodo.app as todo_app

def main_todo(args):
    all_proj_names = [x.name for x in projects_list.get_projects()]
    proj_names = []
    repos = []

    if len(args) > 0:
        projs = [projects_list.get_project(args[0])]
    else:
        projs = projects_list.get_projects()
        
    tasks = []
    for p in projs:
        p.prepare()
        proj_names.append(p.name)
        for repo in p.repos:
            repos.append(repo)

    for repo in repos:
        full_path = projects_list.resolve_dirname(repo)
        new_tasks = todo_app.find_tasks(full_path, repo)
        new_tasks = [t for t in new_tasks if t.extra is None or t.extra not in all_proj_names or t.extra in proj_names]
        tasks += new_tasks

    print('Looking for tasks in {}:'.format(', '.join(repos)))
    os = StringIO()
    todo_app.dump_tasks(tasks, os)
    todo_str = os.getvalue()
    print(todo_str)

    if len(args) > 0:
        projs[0].put_field('todo', todo_str)
    

def main_project(args):
    if len(args) < 1:
        sys.stderr.write('obcontrol-project: Missing action argument\n')
        return 1
    act = args[0]
    args = args[1:]

    if act == 'list':
        projs = projects_list.get_projects()
        for p in projs:
            print('{}\t\t{}'.format(p.name, p.main_file))
        return 0

    else:
        sys.stderr.write('obcontrol-project: Unknown action {}.\n'.format(act))
        return 1

def main(args):
    if len(args) < 1:
        sys.stderr.write('obcontrol: Missing task argument\n')
        return 1
    task = args[0]
    args = args[1:]

    if task == 'project':
        return main_project(args)
    elif task == 'todo':
        return main_todo(args)
    else:
        sys.stderr.write('obcontrol: Unknown task {}.\n'.format(task))
        return 1
