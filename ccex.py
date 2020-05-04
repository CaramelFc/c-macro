#!/usr/bin/env python3
from pathlib import Path
import sys
import re


def find_source_root_dir():
    cwd = Path.cwd()
    while str(cwd) != '/':
        git = cwd / ".git"
        if git.exists():
            return cwd
        cwd = cwd.parent
    raise Exception("Could not find source root dir by .git")


class SearchInclude():
    project_source_dir = find_source_root_dir()
    cwd = Path.cwd()
    flags = []

    def __init__(self, file_name, *args):
        self.file_wd = (self.cwd / file_name).parent
        self.include_path = [self.file_wd]
        self.found = {}
        self.found_path = {str(self.file_wd): "found"}
        if (self.project_source_dir / ".cc_config").exists():
            with open(str(self.project_source_dir / ".cc_config"), "r") as fd:
                lines = fd.readlines()
                for line in lines:
                    if re.match("^-I", line) != None:
                        path = line.replace('\n', '').split('I')[1]
                        abs_path = self.project_source_dir / path
                        if str(abs_path) not in self.found_path:
                            self.found_path[str(abs_path)] = "found"
                            self.include_path.append(abs_path)
                    else:
                        self.flags += " " + line.replace('\n', '')
        self.get_include_flags(file_name)

    def get_include_flags(self, file_name):
        self.dfs(file_name)
        flags = ""
        for path in self.include_path:
            flags += " -I" + str(path)
        for flag in self.flags:
            flags += flag
        print(flags)

    def get_include_file_name(self, file_name):
        ret = []
        with open(file_name, "r") as fd:
            lines = fd.readlines()
            for line in lines:
                if re.match('#include.*".*"$', line) != None:
                    ret.append(line.split('"')[1])
        return ret

    def dfs(self, file_name):
        include_file_name = self.get_include_file_name(file_name)
        if len(include_file_name) == 0:
            return
        for include_file in include_file_name:
            # class: Path
            include_file_path = self.find_file(include_file)
            parent_index = len(include_file.split('/')) - 1
            if include_file_path == None:
                continue
            if str(include_file_path.parents[parent_index]
                   ) not in self.found_path:
                self.found_path[str(
                    include_file_path.parents[parent_index])] = "found"
                self.include_path.append(
                    include_file_path.parents[parent_index])
            if str(include_file_path) not in self.found:
                self.found[str(include_file_path)] = "found"
                self.dfs(str(include_file_path))
            # ...

    def find_file(self, file_name):
        for path in self.include_path:
            file_path = path / file_name
            if file_path.exists():
                return file_path

        # try to search in project_source_dir
        ret = self.search_in_project_source_dir(self.project_source_dir,
                                                file_name)
        if ret == None:
            print("warnning, %s not find, skip it" % (file_name),
                  file=sys.stderr)
        return ret

    def search_in_project_source_dir(self, path, file_name):
        file_path = path / file_name
        if file_path.exists():
            return file_path
        for child in path.iterdir():
            if child.is_dir():
                ret = self.search_in_project_source_dir(child, file_name)
                if ret != None:
                    return ret
        return None


if __name__ == "__main__":
    SearchInclude(sys.argv[1])
