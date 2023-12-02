from aocd import data
import re

dirlists = {}

def cd(cwd, dirname): 
    return cwd + ('' if cwd == '/' else '/') + dirname

def parse(lines):
    dirlists.clear()
    cwd = '/'
    i = 0
    while i < len(lines):
        # switch directories
        match = re.match('^\$ cd (.*)$', lines[i])
        if match:
            dirname = match.group(1)
            if dirname == '/':
                cwd = '/'
            elif dirname == '..':
                cwd = re.match('^((/[^/]+)*)/([^/]+)', cwd).group(1)
                if cwd == '': cwd = ''
            else:
                cwd = cd(cwd, dirname)
            i += 1
            continue
        # list
        if (lines[i] == '$ ls'):
            i += 1
            dirlist = {}
            while i < len(lines) and not(lines[i].startswith('$')):
                match = re.match('^(dir|\d+) (.*)$', lines[i])
                if match.group(1) == 'dir':
                    dirlist[cd(cwd, match.group(2))] = 0
                else:
                    dirlist[match.group(2)] = int(match.group(1))
                i+=1
            dirlists[cwd] = dirlist
            continue
        print('Unexpected line: ' + lines[i])
        break
        

def du(dir):
    dirlist = dirlists[dir]
    sum = 0
    for file,size in dirlist.items():
        if size > 0:
            sum += size
        else:
            sum += du(file)
    return sum

def du_smaller(max):
    sum = 0
    dirs = [k for k in dirlists]
    dirs.append('/')
    for dirname in dirs:
        dirsize = du(dirname)
        if (dirsize <= max):
            sum += dirsize
    return sum

def best_to_delete(fs_size, required):
    free_space = fs_size - du('/')
    needed = required - free_space
    du_list = [du(d) for d in dirlists]
    min_to_remove = fs_size
    for size in du_list:
        if (size < min_to_remove and size > needed):
            min_to_remove = size
    return min_to_remove

ex1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

parse(ex1.splitlines()); 
assert du_smaller(100000) == 95437
assert best_to_delete(70000000, 30000000) == 24933642

parse(data.splitlines()); 
print('7a: ', du_smaller(100000))
print('7b: ', best_to_delete(70000000, 30000000))
