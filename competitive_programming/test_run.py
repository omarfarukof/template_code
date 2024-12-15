#!/usr/bin/env -S uv run
import pytest # noqa: F401
import subprocess
import os
import pycpptest

# Get the name of the Python file
build_dir = "build"
filename = os.path.basename(__file__)
dirname = os.path.dirname(__file__)
problem : str = pycpptest.get_problem(filename)
build_problem : str = os.path.join(build_dir,problem)

# Extract test cases from cph file
testcases = pycpptest.get_test_cases_cph(problem)

def run_problem(input: str  , build_problem=f"{build_problem}")->str:
    return subprocess.check_output([f"./{build_problem}"], input=input.encode('utf-8')).decode('utf-8')
def print_run_problem(input: str  , build_problem=f"{build_problem}")->None:
    print(run_problem(input , build_problem))


## [ Pytest ] ==================================
@pytest.mark.parametrize("test_in , test_out" , testcases)
def test_cph_cases(test_in , test_out):
    assert run_problem(test_in) == test_in


my_testcases = [
    # ("Test_in_01" , "Test_out_01" ),
    # ("Test_in_02" , "Test_out_02" )
]
@pytest.mark.parametrize("my_test_in , my_test_out" , my_testcases)
def test_my_cases(my_test_in, my_test_out):
    assert run_problem(my_test_in) == my_test_out

# Can Generate Test Cases with brute force
def gen_cases(n_cases:int=5 , gen_testcases:list[tuple[str, str]]=[]) -> list[tuple[str, str]]:
    # TODO: Generate test cases with brute force        
    # 
    # 
    return gen_testcases

@pytest.mark.parametrize("gen_test_in , gen_test_out" , gen_cases())
def test_gen_cases(gen_test_in , gen_test_out):
    assert run_problem(gen_test_in) == gen_test_out
    
    
## [ Main ] (run from Script) ==================
if __name__ == "__main__":
    pycpptest.compile(problem , build_dir)
    filepath = os.path.join(dirname,filename)
    os.system(f"pytest -vv {filepath}")