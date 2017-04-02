#!/usr/bin/env python
# Author: Jayden Navarro

class ProjectNameError( Exception ):
   pass

def full_project_name( proj_name, project_list ):
   projects = dict( project_list ).keys()

   # check for exact matches first
   exact_matches = [ name for name in projects if proj_name == name ]
   if len( exact_matches ) == 1:
      return exact_matches[ 0 ]

   # check for substring matches
   full_names = [ name for name in projects if proj_name in name ]
   if len( full_names ) == 1:
      return full_names[ 0 ]
   elif len( full_names ) == 0:
      raise ProjectNameError( 'No matching projects found' )
   else:
      raise ProjectNameError( 'Ambigous project name, following match: %s' \
         % ', '.join( full_names ) )
