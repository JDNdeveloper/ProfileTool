#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from profile_tool import profile_tool
from proj_helper import full_project_name

parser = argparse.ArgumentParser( description='change default package' )
parser.add_argument( 'package', type=str, help='new default package' )
parser.add_argument( '--project', type=str, default=os.environ[ 'CURR_WS' ],
                     help='project name (default is current project)' )

args = parser.parse_args()
pkg_name = args.package
proj_name = args.project

pt = profile_tool()
groups = pt.readGroups()
projects = dict( groups[ 'projects' ] )
full_proj_name = full_project_name( proj_name, projects.items() )
projects[ full_proj_name ] = pkg_name
groups[ 'projects' ] = projects.items()
pt.writeGroups( groups )
