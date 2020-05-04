#!/usr/bin/env python3
import re
import sys


class StripInclude():
    def __init__(self, src_file, intermediate_file):
        with open(src_file, "r") as fd1, open(intermediate_file, "r") as fd2:
            src_lines = fd1.readlines()
            inter_lines = fd2.readlines()
            index_lines = [1]
            for index, line in enumerate(src_lines):
                if re.match("^#include", line):
                    index_lines.append(index + 1)
            while len(index_lines) > 0:
                start = index_lines[0]
                l = -1
                r = -1
                for index, line in enumerate(inter_lines):
                    if re.match("^#.*" + src_file, line):
                        if l != -1:
                            r = index
                            break
                        inter_index = int(line.split(' ')[1])
                        if l == -1:
                            if inter_index <= start:
                                l = index
                            else:
                                # may deprecate by macro
                                break
                assert (l == -1 and r == -1 or l != -1 and r != -1)
                if l != -1 and r != -1:
                    assert (int(inter_lines[l].split(' ')[1]) <= start
                            and int(inter_lines[r].split(' ')[1]) >= start)
                if l != -1 and r != -1:
                    del inter_lines[l:r]
                del index_lines[0]
            for line in inter_lines:
                print(line, end='')


if __name__ == "__main__":
    StripInclude(sys.argv[1], sys.argv[2])
