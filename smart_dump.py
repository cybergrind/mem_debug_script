#!/usr/bin/env python3
import argparse
import logging
from fan_tools.unix import succ
from pathlib import Path
from pprint import pprint


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger('LOG_NAME')


def parse_args():
    parser = argparse.ArgumentParser(description='DESCRIPTION')
    # parser.add_argument('-m', '--mode', default='auto', choices=['auto', 'manual'])
    # parser.add_argument('-l', '--ll', dest='ll', action='store_true', help='help')
    return parser.parse_args()


FILTER = ['onKeyUp_MENU_CLICK',
          'OnLoaded',
          'OnLevelLoaded',
          'OnPvpDefaultLoadoutCreated',
          'OnLocalAvatarCreated',
          'cterCreated',
          'Created customization of type',
          'SpawnFriendlyAgent',
          'CreateLoadOutLoader']

def print_created(out):
    for line in out:
        for skip in FILTER:
            if skip in line:
                break
        else:
            print(f'found: {line}')


def dump():
    pid_list = succ('pgrep -f "Warframe.x64"')[1]
    pid = pid_list[0]
    print(f'Got: {pid=}')
    maps = Path(f'/proc/{pid}/maps').read_text().split('\n')
    for mem in maps:
        if not mem:
            continue
        s = mem.split()[0].split('-')
        start, end = map(lambda x: int(x, 16), s)
        size = end - start
        if size > 800348928:
            print(f'{mem=} => {end - start=}')
            fname = f'{pid}-{s[0]}-{s[1]}.dump'
            cmd = f'gdb --batch --pid {pid} -ex "dump memory {fname} 0x{s[0]} 0x{s[1]}"'
            succ(cmd)
            print(f'Wrote: {fname=} {cmd=}')
            _, out, _ = succ(f'strings {fname} | ag "Created "')
            print(f'{out=}')
            print_created(out)



def main():
    args = parse_args()
    dump()


if __name__ == '__main__':
    main()


