#!/usr/bin/env python3
import argparse
import logging
from contextlib import suppress
from pathlib import Path

from fan_tools.unix import succ


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("LOG_NAME")


def parse_args():
    parser = argparse.ArgumentParser(description="DESCRIPTION")
    # parser.add_argument('-m', '--mode', default='auto', choices=['auto', 'manual'])
    # parser.add_argument('-l', '--ll', dest='ll', action='store_true', help='help')
    return parser.parse_args()


FILTER = [
    "onKeyUp_MENU_CLICK",
    "OnLoaded",
    "OnLevelLoaded",
    "OnPvpDefaultLoadoutCreated",
    "OnLocalAvatarCreated",
    "cterCreated",
    "Created customization of type",
    "SpawnFriendlyAgent",
    "CreateLoadOutLoader",
]


def print_created(out):
    for line in out:
        for skip in FILTER:
            if skip in line:
                break
        else:
            print(f"found: {line}")


class MemTxt:
    def __init__(self, s, pid):
        self.s = s
        self.pid = pid
        self.t = s.split()
        self.addrs = self.t[0]
        ss = self.addrs.split("-")
        self.hstart, self.hend = ss
        self.start, self.end = map(lambda x: int(x, 16), ss)
        self.size = self.end - self.start
        self.is_rw = self.t[1].startswith('rw')
        self.system = self.fname.startswith('/')
        self.is_wf = self.fname == self.fname.endswith('Warframe.x64.exe')
        print(f"{len(self.t)=} {self.t}")

    @property
    def fname(self):
        if len(self.t) == 5:
            return ''
        return self.t[5]

    def dump(self):
        fname = f"{self.pid}-{self.addrs}.dump"
        mem_range = f'0x{self.hstart} 0x{self.hend}'
        cmd = f'gdb --batch --pid {self.pid} -ex "dump memory {fname} {mem_range}"'
        print(f'Dump to: {fname}')
        succ(cmd)


def dump():
    pid_list = succ('pgrep -f "Warframe.x64"')[1]
    pid = pid_list[0]
    print(f"Got: {pid=}")
    maps = Path(f"/proc/{pid}/maps").read_text().split("\n")
    for mem in maps:
        if not mem:
            continue
        mreg = MemTxt(mem, pid)
        if 0x140000000 <= mreg.start < 0x143175000:
            mreg.dump()
            continue
        if mreg.size < 2 * 1024 * 1024:
            continue
        if mreg.system or not mreg.is_rw:
            continue
        mreg.dump()
        continue
        tpl = mem.split()
        addrs = tpl[0]
        perms = tpl[1]

        print(f"{tpl=}")
        s = addrs[0].split("-")
        start, end = map(lambda x: int(x, 16), s)
        size = end - start
        print(f"{mem=} => {end - start=}")
        # 591917056 / 800348928 / 387383296
        if size > 347383296:
            fname = f"{pid}-{s[0]}-{s[1]}.dump"
            cmd = f'gdb --batch --pid {pid} -ex "dump memory {fname} 0x{s[0]} 0x{s[1]}"'
            succ(cmd)
            print(f"Wrote: {fname=} {cmd=}")
            with suppress(ExecError):
                _, out, _ = succ(f'strings {fname} | ag "Created "')
                print(f"{out=}")
                print_created(out)


def main():
    args = parse_args()
    dump()


if __name__ == "__main__":
    main()
