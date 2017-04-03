#!/usr/bin/env python
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
