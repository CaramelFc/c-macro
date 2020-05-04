## Description

small utility written by python for macro expansion in c and c++

## Usag

```shell
./ccex.py <input.cpp> | xargs g++ -E <input.cpp> > <intermediate.cpp>
./ccstrip.py <intermediate.cpp> > <output.cpp>
```

Note that the `input.cpp` must in a repo with git
You can look `output.cpp` for result of macro expansion 
You can set more compilation flags for macro expansion in `.cc_config`
```shell
cp cc_config.example path/to/repo_with_git/.cc_config
```

