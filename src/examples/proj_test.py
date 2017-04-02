#!/usr/bin/env python
# Author: Jayden Navarro

import os
from shutil import copyfile
import profile_tool as pt

from default_pkg import default_pkg
from delete_proj import delete_proj
from new_proj import new_proj
from switch_proj import switch_proj

from proj_helper import full_project_name, ProjectNameError

orig_profile = '../example_profile'
test_profile = 'test_profile'

def getDefaultProject( groups ):
   return groups[ 'default_project' ][ 0 ][ 0 ]

def getProjects( groups ):
   return dict( groups[ 'projects' ] )

def setDefaultProject( proj_name, groups ):
   groups[ 'default_project' ] = [ ( proj_name, ) ]

def setProjects( projects, groups ):
   groups[ 'projects' ] = projects.items()

def runTest():
   copyfile( orig_profile, test_profile )

   ptool = pt.profile_tool( test_profile )

   proj_name_1 = 'Proj_Test_1'
   proj_name_2 = 'Proj_Test_2'

   pkg_name_1 = 'Pkg_Test_1'
   pkg_name_2 = 'Pkg_Test_2'

   # NEW_PROJ test

   # no default, empty package name
   proj_name = proj_name_1
   groups = ptool.readGroups()
   pkg_name = ''
   assert proj_name not in getProjects( groups )
   new_proj( proj_name, pkg_name, False, profile=test_profile )
   groups = ptool.readGroups()
   assert proj_name in getProjects( groups )
   assert proj_name != getDefaultProject( groups )
   assert pkg_name == getProjects( groups )[ proj_name ]

   # default, with pacakge name
   proj_name = proj_name_2
   pkg_name = pkg_name_2 
   groups = ptool.readGroups()
   assert proj_name not in getProjects( groups )
   new_proj( proj_name, pkg_name, True, profile=test_profile )
   groups = ptool.readGroups()
   assert proj_name in getProjects( groups )
   assert proj_name == getDefaultProject( groups )
   assert pkg_name == getProjects( groups )[ proj_name ]


   # DELETE_PROJ test

   # delete non-default project
   proj_name = proj_name_1
   groups = ptool.readGroups()
   assert proj_name in getProjects( groups )
   assert proj_name != getDefaultProject( groups )
   delete_proj( proj_name, profile=test_profile )
   groups = ptool.readGroups()
   assert proj_name not in getProjects( groups )

   # delete default project, verify top project is now default
   proj_name = proj_name_2
   groups = ptool.readGroups()
   assert proj_name in getProjects( groups )
   assert proj_name == getDefaultProject( groups )
   delete_proj( proj_name, profile=test_profile )
   groups = ptool.readGroups()
   assert proj_name not in getProjects( groups )
   assert proj_name != getDefaultProject( groups )
   top_project = groups[ 'projects' ][ 0 ][ 0 ]
   assert top_project == getDefaultProject( groups )

   # re-add projs for rest of tests
   new_proj( proj_name_1, pkg_name_1, False, profile=test_profile )
   new_proj( proj_name_2, pkg_name_2, True, profile=test_profile )


   # SWITCH_PROJ test

   # switch to non-default project
   proj_name = proj_name_1
   groups = ptool.readGroups()
   assert proj_name != getDefaultProject( groups )
   switch_proj( proj_name, profile=test_profile )
   groups = ptool.readGroups()
   assert proj_name == getDefaultProject( groups )


   # DEFAULT_PKG test

   # no project name (uses default project)
   proj_name = proj_name_1
   pkg_name_old = pkg_name_1
   pkg_name_new = pkg_name_2
   groups = ptool.readGroups()
   assert pkg_name_old == getProjects( groups )[ proj_name ]
   default_pkg( pkg_name_new, proj_name, profile=test_profile )
   groups = ptool.readGroups()
   assert pkg_name_new == getProjects( groups )[ proj_name ]


   # FULL_PROJECT_NAME test

   # setup for project name test
   fpn_exact = 'fpn_'
   fpn_a = 'fpn_a'
   fpn_b = 'fpn_b'
   fpn_full = 'fpn_unique_one'
   new_proj( fpn_exact, '', False, profile=test_profile )
   new_proj( fpn_a, '', False, profile=test_profile )
   new_proj( fpn_b, '', False, profile=test_profile )
   new_proj( fpn_full, '', False, profile=test_profile )
   fpn_ambiguous = 'fpn'
   fpn_sub = 'fpn_unique'
   fpn_none = 'fpn_none'
   groups = ptool.readGroups()
   projects = getProjects( groups )

   # exact match
   assert fpn_a == full_project_name( fpn_a, projects )

   # substring match
   assert fpn_full == full_project_name( fpn_sub, projects )

   # no matches
   try:
      full_project_name( fpn_none, projects )
   except ProjectNameError:
      pass
   else:
      assert False

   # multiple matches
   try:
      full_project_name( fpn_ambiguous, projects )
   except ProjectNameError:
      pass
   else:
      assert False

   # exact match with multiple substring match
   assert fpn_exact == full_project_name( fpn_exact, projects )

   os.remove( test_profile )

if __name__ == '__main__':
   runTest()
   print "TEST PASSED"

