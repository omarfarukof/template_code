#!/usr/bin/env -S uv run
import json
import os
import subprocess
import sys
# VS Code runCommand parameters
# "CreateTestPy": "mkdir -p ${workspaceFolder}/test && cp -n ${homedir}/Project/template_code/competitive_programming/pycpptest.py ${workspaceFolder}/test/pycpptest.py &&  cp ${homedir}/Project/template_code/competitive_programming/test_run.py ${workspaceFolder}/test/test_${fileBasenameNoExtension}.py && chmod +x ${workspaceFolder}/test/test_${fileBasenameNoExtension}.py",
# "RunCppTest": "${workspaceFolder}/test/test_${fileBasenameNoExtension}.py",
# 
# `test_run.py` file is need as template for pytest

def get_problem(filename: str) -> str:
    ext_len = len(filename.split(".")[-1])+1
    if filename[:5] == "test_":
        return filename[5:-ext_len]
    else:
        return filename[:-ext_len]

def get_test_cases_cph(problem: str , testcases = []) -> list[tuple[str, str]]:
    dirname = os.path.dirname(__file__)
    working_dir = dirname[:-(len("test"))] if dirname[-(len("test")):] == "test" else dirname
    cph_path = os.path.join(working_dir,".cph")
    if not os.path.exists(cph_path):
        return testcases

    cph_file = None
    files = os.listdir(cph_path)
    for file in files:
        if file.startswith(f".{problem}"):
            cph_file = os.path.join(cph_path,file)
            break
    if cph_file is not None:
        with open(cph_file, 'r') as f:
            cph = json.load(f)
            f.close()

        tests = cph["tests"]
        for test in tests:
            test_in = test["input"]
            test_out = test["output"]
            testcases.append((test_in , test_out))

    return testcases

def compile(problem: str , build_dir: str , compiler: str = "cpp") -> None:
    # make a build directory if it doesn't exist
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    build_problem : str = os.path.join(build_dir,problem)
    if compiler == "cpp":
        subprocess.run(["g++","-fsanitize=address","-std=c++20",
            "-Wall","-Wextra","-Wshadow","-O2",
            f"./{problem}.cpp" , "-o", f"{build_problem}"])
    else:
        print("Error: Compiler is not implemented")
        sys.exit(1)

