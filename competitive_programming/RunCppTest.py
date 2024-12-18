#!/usr/bin/env -S uv run

import sys
import pycpptest as pct

if len(sys.argv) == 2:
    pct.RunCppTest(sys.argv[1] )
elif len(sys.argv) == 3:
    pct.RunCppTest(sys.argv[1] , test_path=sys.argv[2])
else:
    print("Error: Invalid number of arguments")
    sys.exit(1)

