#!/usr/bin/env -S uv run
import json
import os
import subprocess
import sys
import json

DEBUG = False
DEBUG_rm_tmp_files = False
RM_TMP = True
DEBUG_run_problem = False
DEBUG_testcases = [
    # ("Test_in_01" , "Test_out_01" ),
    # ("Test_in_02" , "Test_out_02" )
    ("Omar\n", "Hello Omar\n"),
    ("Omar Faruk\n", "Hello Omar Faruk\n")
]

sub_prefix = "|"+"-"*4
msg_len = 80

color_code = {
    "red": 91,
    "green": 92,
    "yellow": 93,
    "blue": 94,
    "magenta": 95,
    "cyan": 96,
    "white": 97,
    "reset": 0
}
def get_color_code(color: str) -> str:
    return f"\033[{color_code[color]}m"

# VS Code runCommand parameters
# "CreateTestPy": "mkdir -p ${workspaceFolder}/test && cp -n ${homedir}/Project/template_code/competitive_programming/pycpptest.py ${workspaceFolder}/test/pycpptest.py &&  cp ${homedir}/Project/template_code/competitive_programming/test_run.py ${workspaceFolder}/test/test_${fileBasenameNoExtension}.py && chmod +x ${workspaceFolder}/test/test_${fileBasenameNoExtension}.py",
# "RunCppTest": "${workspaceFolder}/test/test_${fileBasenameNoExtension}.py",
# 
# `test_run.py` file is need as template for pycpptest


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

def r_print(text:str, console=True)->str|None:
    if console:
        print(f"\033[91m{text}\033[0m")
    else:
        return (f"\033[91m{text}\033[0m")

def g_print(text:str, console=True)->str|None:
    if console:
        print(f"\033[92m{text}\033[0m")
    else:
        return (f"\033[92m{text}\033[0m")

def b_print(text:str, console=True)->str|None:
    if console:
        print(f"\033[94m{text}\033[0m")
    else:
        return (f"\033[94m{text}\033[0m")

def col_print(text:str, color: str, console=True)->str|None:
    if console:
        print(f"{get_color_code(color)}{text}{get_color_code('reset')}")
    else:
        return (f"{get_color_code(color)}{text}{get_color_code('reset')}")
        

def center_print(text:str, prt=b_print , console=True, char="_")->str|None:
    text = "[" + char*int((msg_len-len(text))/2) + text + char*int((msg_len-len(text))/2) + "]"
    prt(text , console=console)

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


def run_problem(input: str  , build_problem , benchmark=False , c_print=False)->str|None:
    if DEBUG:
        col_print(f"Benchmark Status: {benchmark}", color="yellow")
    # b_print(f"CMD: {' '.join(build_problem_cmd)}")
    in_out_cmd = ["<", "tmp_input.txt", ">", "tmp_output.txt"]
    # rm_in_out_cmd = ["rm", "-f", "tmp_input.txt", "tmp_output.txt"]
    if not os.path.exists(build_problem):
        r_print(f"Error:Compiled File ({build_problem}) does not exist")
        sys.exit(1)

    build_problem_cmd = ["./"+build_problem]
    benchmark_cmd = [ "\\time", "-f", "\"{\'Program\': %C,\'Total time\': %e,\'User Mode\': %U,\'Kernel Mode\': %S,\'CPU\': %P,\'Memory(RSS)\':%M,\'Memory(Avg)\':%t,\'Memory(Avg Total)\': %K}\" " ]
    # if benchmark:
    #     build_problem_cmd = benchmark_cmd + ["\n"] + build_problem_cmd
    
    build_problem_cmd.extend(in_out_cmd)

    with open("tmp_input.txt" , "w") as f_in:
        f_in.write(input)
        f_in.close()

    if DEBUG_run_problem:
        col_print(f"\n[From: pycpptest.py>run_problem]\nCMD: {(build_problem_cmd)}", color="yellow")

    # process = subprocess.run(
    #     build_problem_cmd,
    #     # input=input.encode('utf-8'), 
    #     capture_output=True)
    with open("tmp_run.sh" , "w") as f_run:
        f_run.write("#!/bin/bash\n")
        if benchmark:
            f_run.write(" ".join(benchmark_cmd[:2]))
            # f_run.write(" \\n Benchmark Result: \\n")
            f_run.write((benchmark_cmd[2]).replace(","," \\n").replace("{","{  Benchmark Result:\n").replace("}","}\n"))
        f_run.write(" ".join(build_problem_cmd))
        # f_run.write(" ".join(rm_in_out_cmd))
        f_run.close()
    
    benchmark_result = subprocess.check_output(["bash" , "tmp_run.sh"])
    with open("benchmark_result.json" , "w") as f_bench:
        f_bench.write(benchmark_result.decode('utf-8'))
        f_bench.close()
    # b_print(f"\nReturn Code: {process.returncode}")
    with open("tmp_output.txt" , "r") as f_out:
        output = f_out.read()
        f_out.close()

    

    # if c_print:
    #     print(process.stdout)
    # else:
    #     return process.stdout

    # return ""
    if RM_TMP:
        rm_tmp_files()
    return output

def rm_tmp_files(path=".")->None:
    if DEBUG_rm_tmp_files:
        col_print("ls:", color="yellow")
        print(os.listdir(path))
    rm_files =[ x for x in os.listdir(path) if x.startswith("tmp_")]
    if DEBUG_rm_tmp_files:
        col_print("ls:", color="yellow")
        print(rm_files)
    for rm_file in rm_files:
        os.remove(rm_file)

def output_failure_result(input , run_output , expected_output, Test_Case_No , No_Cases, Test_Name="" , prefix="")->None:
    r_print(f"{prefix+sub_prefix} Failed {Test_Name} Test Case {Test_Case_No} of {No_Cases}\n")
    center_print(f"Status Result: {Test_Name} {Test_Case_No}/{No_Cases}" , char=" ")
    b_print(f"[ Input: ] {'='*(msg_len-len("[ Input: ]"))}")
    b_print("-"*msg_len+">")
    print(f"{input}")
    b_print(f"[ Expected Output:] {'='*(msg_len-len("[ Expected Output:]"))}")
    b_print("-"*msg_len+">")
    print(f"{expected_output}")
    b_print(f"[ Run Output: ] {'='*(msg_len-len("[ Run Output: ]"))}")
    b_print("-"*msg_len+">")
    print(f"{run_output}")
    b_print('-'*msg_len)
    center_print("Status Result:" , char=" ")


def test_single_case(test_in , test_out , build_problem , verify_output, benchmark=False , Test_Case_No=1, No_Cases=1, Test_Name="" , prefix="")->bool:
    input = test_in
    run_output = run_problem(input, build_problem , benchmark=benchmark)
    expected_output = test_out
    if verify_output(input, run_output, expected_output):
        g_print(f"\t{prefix+sub_prefix} Passed {Test_Name} Test Case {Test_Case_No} of {No_Cases}")
        return True
    else:
        output_failure_result(input , run_output , expected_output, Test_Case_No, No_Cases , Test_Name=Test_Name , prefix=prefix+"\t")
        return False
        

def test_code(testcases , build_problem , verify_output, benchmark=False , Test_Name="Test", prefix="")->None:
    # g_print("/"+"="*40+"\\")
    g_print(f"\n[ Test {Test_Name} ] " + "="*(msg_len-len(f"[ Test {Test_Name} ]"))+"]")

    No_Cases = len(testcases)
    test_status: bool|None = None 
    if No_Cases == 0:
        col_print(f"{prefix}|{'-'*4} Skipping {Test_Name} TestCases", color="yellow")
    else:
        b_print(f"{prefix}|{'-'*4} Running {No_Cases} TestCases from {Test_Name}")
    for i in range(len(testcases)):
        b_print(f"{prefix}\t|{'-'*4} ({i+1}) Running Test Case {i+1} of {No_Cases}")
        test_in , test_out = testcases[i]
        test_status = test_single_case(test_in , test_out, build_problem , verify_output, benchmark=benchmark , Test_Case_No=i+1, No_Cases=No_Cases , Test_Name=Test_Name , prefix=prefix+"\t")
    
    print()
    if test_status is None:
        center_print(f"[ Test {Test_Name} Skipped ]")
    elif not test_status:
        center_print(f"[ Test {Test_Name} Failed ]", prt=r_print)
    else:
        center_print(f"[ Test {Test_Name} Passed ]", prt=g_print)