#!/usr/bin/env python
# Author: Jayden Navarro

from profile_tool import profile_tool

class ProjectNameError( Exception ):
   pass

def check_groups( func ):
   def inner( self, *args, **kwargs ):
      if self.groups_ is None:
         raise ValueError( 'groups is None' )
      else:
         return func( self, *args, **kwargs )
   return inner

class proj_helper(object):
   def __init__( self, profile, groups=None ):
      self.ptool_ = profile_tool( profile )
      self.groups_ = groups

   def read_profile( self ):
      self.groups_ = self.ptool_.readGroups()

   @check_groups
   def write_profile( self ):
      self.ptool_.writeGroups( self.groups_ )

   @property
   @check_groups
   def default_project( self ):
      try:
         return self.groups_[ 'default_project' ][ 0 ][ 0 ]
      except:
         return ''

   @default_project.setter
   @check_groups
   def default_project( self, proj_name ):
      self.groups_[ 'default_project' ] = [ ( proj_name, ) ]

   @property
   @check_groups
   def projects( self ):
      try:
         return dict( self.groups_[ 'projects' ] )
      except:
         return {}

   @projects.setter
   @check_groups
   def projects( self, projects ):
      self.groups_[ 'projects' ] = projects.items()

   @check_groups
   def get_full_project_name( self, proj_name ):
      projects = self.projects
      
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
