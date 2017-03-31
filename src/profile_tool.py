#!/usr/bin/env python
# Author: Jayden Navarro

import re
import os
import capture_groups as cg

homeDir = os.path.expanduser( '~' )
bashrc_path = homeDir + '/.bashrc'

class profile_tool:
   def __init__( self, profile_path=bashrc_path ):
      self._profile_path = profile_path
      self._pt_start_re = r'# pt_start (.*)'
      self._pt_end_re = r'# pt_end (.*)'

   def readGroups( self ):
      groups = {}

      with open( self._profile_path, 'r' ) as f:
         lines = f.readlines()
         capture = []
         capture_group = ''
         for line in lines:
            # handle pt control tokens
            pt_start_group = re.findall( self._pt_start_re, line )
            pt_end_group = re.findall( self._pt_end_re, line )
            if pt_start_group:
               capture_group = pt_start_group[ 0 ]
            elif pt_end_group:
               # end of capture, get the group re from group name
               group_re = getattr( cg, 'rgx_' + capture_group )

               matches = []
               # for all regex provided for group, add them to matches
               for regex in group_re:
                  matches.append( re.findall( regex, ''.join( capture ) ) )
               # zip all matches together to pair up fields
               groups[ capture_group ] = zip( *matches )

               # reset capture
               capture_group = ''
               capture = []
            elif capture_group:
               # if capture_group is valid, append output
               capture.append( line )
      return ( groups )

   def writeGroups( self, groups ):
      def render( group_name, data ):
         group_format = getattr( cg, 'fmt_' + group_name )
         return ''.join( [ group_format % matches for matches in data ] )
      
      with open( self._profile_path, 'r+' ) as f:
         lines = f.readlines()
         output_lines = []
         capture_group = ''
         for line in lines:
            # handle pt control tokens
            pt_start_group = re.findall( self._pt_start_re, line )
            pt_end_group = re.findall( self._pt_end_re, line )
            if pt_start_group:
               capture_group = pt_start_group[ 0 ]
            elif pt_end_group:
               output_lines.append(
                  render( capture_group, groups[ capture_group ] ) )
               capture_group = ''
            elif capture_group:
               continue
            output_lines.append( line )
         f.seek( 0 )
         f.write( ''.join( output_lines ) )
         f.truncate()

if __name__ == '__main__':
   tmp_profile_path = '/home/jayden/.bashrc.tmp'
   p = profile_tool( tmp_profile_path )
   groups = p.readGroups()
   groups[ 'default_project' ][ 0 ] = ( 'bob.0', )
   p.writeGroups( groups )
