#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from proj_helper import proj_helper

def new_proj( proj_name, pkg_name, default, profile='' ):
   ph = proj_helper( profile )
   ph.read_profile()
   projects = ph.projects
   if proj_name in projects:
      print 'Project already exists'
      exit( 1 )
   elif proj_name == '':
      print 'Project name cannot be empty'
      exit( 1 )
   projects[ proj_name ] = pkg_name
   ph.projects = projects
   if default:
      ph.default_project = proj_name
   ph.write_profile()

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='add project' )
   parser.add_argument( 'project', type=str, help='project name' )
   parser.add_argument( 'package', type=str, nargs='?', default='',
                        help='default package' )
   parser.add_argument( '--default', action='store_true',
                        help='set project as default' )
                     
   args = parser.parse_args()
   proj_name = args.project
   pkg_name = args.package
   default = args.default

   new_proj( proj_name, pkg_name, default )
