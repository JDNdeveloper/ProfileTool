#!/usr/bin/env python2
# Author: Jayden Navarro

import argparse
import os
import sys
from proj_helper import proj_helper

def switch_parent( proj_name, parent_name, profile='' ):
   ph = proj_helper( profile )
   ph.read_profile()
   full_proj_name = ph.get_full_project_name( proj_name )
   projects = ph.projects
   pkg_name, proj_type, _old_parent = projects[ full_proj_name ]
   projects[ full_proj_name ] = ( pkg_name, proj_type, parent_name )
   ph.projects = projects
   ph.write_profile()

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='change project parent' )
   parser.add_argument( 'project', type=str, help='project name' )
   parser.add_argument( 'parent', type=str, help='new parent project name' )

   args = parser.parse_args()
   switch_parent( args.project, args.parent )
