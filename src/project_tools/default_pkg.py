#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from proj_helper import proj_helper

def default_pkg( pkg_name, proj_name, profile='' ):
   ph = proj_helper( profile )
   ph.read_profile()
   full_proj_name = ph.get_full_project_name( proj_name )
   projects = ph.projects
   old_pkg_name, proj_type = projects[ full_proj_name ]
   projects[ full_proj_name ] = ( pkg_name, proj_type )
   ph.projects = projects
   ph.write_profile()

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='change default package' )
   parser.add_argument( 'package', type=str, help='new default package' )
   parser.add_argument( '--project', type=str, default=os.environ[ 'CURR_WS' ],
                        help='project name (default is current project)' )

   args = parser.parse_args()
   pkg_name = args.package
   proj_name = args.project

   default_pkg( pkg_name, proj_name )
