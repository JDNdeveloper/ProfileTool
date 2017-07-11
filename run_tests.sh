#!/usr/bin/bash

cwd=$(pwd)

# run profile_tool_test
cd ${cwd}/src/
python profile_tool_test.py

# run 
cd ${cwd}/src/project_tools
python proj_test.py
