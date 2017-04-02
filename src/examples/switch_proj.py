#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from profile_tool import profile_tool
from proj_helper import full_project_name

def switch_proj( proj_name, profile='' ):
   if profile:
      pt = profile_tool( profile )
   else:
      pt = profile_tool()
   groups = pt.readGroups()
   default_proj = full_project_name( proj_name, groups[ 'projects' ] )
   groups[ 'default_project' ] = [ ( default_proj, ) ]
   pt.writeGroups( groups )

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='add project' )
   parser.add_argument( 'project', type=str, help='project name' )

   args = parser.parse_args()
   proj_name = args.project

   switch_proj( proj_name )
