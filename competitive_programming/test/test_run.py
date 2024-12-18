#!/usr/bin/env -S uv run

import os
import pycpptest as pct

# Get the name of the Python file
build_dir = "build"
filename = os.path.basename(__file__)
dirname = os.path.dirname(__file__)
problem : str = pct.get_problem(filename)
build_problem : str = os.path.join(build_dir,problem)

# Extract test cases from cph file
cph_testcases = pct.get_test_cases_cph(problem)

my_testcases = [
    # ("Test_in_01" , "Test_out_01" ),
    # ("Test_in_02" , "Test_out_02" )
]

gen_testcases = []

def verify_output(input , run_output, expected_output, match_char=True)->bool:
    if match_char:
        return run_output == expected_output
    else:
        # TODO: Write Verification Logic
        # 
        #         
        return False

# Can Generate Test Cases with brute force
def gen_cases(n_cases:int=5 , gen_testcases:list[tuple[str, str]]=[]) -> list[tuple[str, str]]:
    # TODO: Generate test cases with brute force        
    # 
    # 
    return gen_testcases



## [ PyCpptest ] ==================================

def test_cases(test_in , test_out , build_problem , Test_Case_No=1, No_Cases=1)->bool:
    input = test_in
    run_output = pct.run_problem(input, build_problem)
    expected_output = test_out
    if verify_output(input, run_output, expected_output):
        pct.g_print(f"Passed CPH Test Case {Test_Case_No} of {No_Cases}")
        return True
    else:
        pct.output_failure_result(input , run_output , expected_output, Test_Case_No, No_Cases)
        return False

    
## [ Main ] (run from Script) ==================
if __name__ == "__main__":
    pct.center_print(" PyCpptest Start " , char="=")
    pct.compile(problem , build_dir)
    filepath = os.path.join(dirname,filename)

    # CPH_TestCases
    pct.test_code(cph_testcases , build_problem , verify_output , Test_Name="CPH")

    # My_TestCases
    pct.test_code(my_testcases , build_problem , verify_output , Test_Name="MY")

    # Gen_TestCases
    gen_testcases = gen_cases(gen_testcases=[])
    pct.test_code(gen_testcases , build_problem , verify_output , Test_Name="GEN")

    if pct.DEBUG:
        pct.test_code(pct.DEBUG_testcases , build_problem , verify_output, benchmark=True , Test_Name="DEBUG")

