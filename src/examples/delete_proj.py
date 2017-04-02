#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from profile_tool import profile_tool
from proj_helper import full_project_name

parser = argparse.ArgumentParser( description='delete project' )
parser.add_argument( 'project', type=str, help='project name' )

args = parser.parse_args()
proj_name = args.project

if proj_name == os.environ[ 'CURR_WS' ]:
   print "can't delete the workspace you're currently in"
   exit( 1 )

pt = profile_tool()
groups = pt.readGroups()
projects = dict( groups[ 'projects' ] )
full_proj_name = full_project_name( proj_name, projects.items() )
del projects[ full_proj_name ]
if full_proj_name == groups[ 'default_project' ][ 0 ][ 0 ]:
   # if deleted project was default, change default project to
   # the first other project in the dictionary of projects
   groups[ 'default_project' ] = [ ( projects.keys()[ 0 ], ) ]
groups[ 'projects' ] = projects.items()
pt.writeGroups( groups )
