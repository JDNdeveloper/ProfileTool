#!/usr/bin/env python2
# Author: Jayden Navarro

import argparse
import os
import sys
from proj_helper import proj_helper

def delete_proj( proj_name, profile='' ):
   if proj_name == os.environ.get( 'CURR_WS', '' ):
      print "can't delete the workspace you're currently in"
      exit( 1 )

   ph = proj_helper( profile )
   ph.read_profile()
   projects = ph.projects
   full_proj_name = ph.get_full_project_name( proj_name )

   # Re-parent any children onto the deleted project's own parent. Without
   # this, a stacked child keeps a CURR_PARENT pointer to a project (and
   # branch) that no longer exists, which breaks rebaseat with "fatal:
   # invalid upstream" on the next run.
   _pkg, _type, deleted_parent = projects[ full_proj_name ]
   for child_name, ( child_pkg, child_type, child_parent ) in projects.items():
      if child_parent == full_proj_name:
         projects[ child_name ] = ( child_pkg, child_type, deleted_parent )
         print "reparented '%s' from '%s' to '%s'" % (
            child_name, full_proj_name, deleted_parent or 'main' )

   del projects[ full_proj_name ]
   if full_proj_name == ph.default_project:
      # if deleted project was default, change default project to
      # the first other project in the dictionary of projects if
      # there are more projects
      if projects:
         ph.default_project = projects.keys()[ 0 ]
      else:
         ph.default_project = ''
   ph.projects = projects
   ph.write_profile()

if __name__ == '__main__':
   parser = argparse.ArgumentParser( description='delete project' )
   parser.add_argument( 'project', type=str, help='project name' )

   args = parser.parse_args()
   proj_name = args.project

   delete_proj( proj_name )
