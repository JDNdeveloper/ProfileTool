#!/usr/bin/env python
# Author: Jayden Navarro

import argparse
import os
import sys
from profile_tool import profile_tool

def new_proj( proj_name, pkg_name, default, profile='' ):
   if profile:
      pt = profile_tool( profile )
   else:
      pt = profile_tool()
   groups = pt.readGroups()
   projects = dict( groups[ 'projects' ] )
   if proj_name in projects:
      print 'Project already exists'
      exit( 1 )
   projects[ proj_name ] = pkg_name
   groups[ 'projects' ] = projects.items()
   if default:
      groups[ 'default_project' ] = [ ( proj_name, ) ]
   pt.writeGroups( groups )

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
