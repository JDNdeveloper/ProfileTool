#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from proj_helper import proj_helper

def switch_proj( proj_name, profile='' ):
   ph = proj_helper( profile )
   ph.read_profile()
   projects = ph.projects
   full_project_name = ph.get_full_project_name( proj_name )
   ph.default_project = full_project_name
   ph.write_profile() 

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='add project' )
   parser.add_argument( 'project', type=str, help='project name' )

   args = parser.parse_args()
   proj_name = args.project

   switch_proj( proj_name )
