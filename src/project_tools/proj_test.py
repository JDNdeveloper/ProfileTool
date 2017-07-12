#!/usr/bin/env python
# Author: Jayden Navarro

import os
from shutil import copyfile

from default_pkg import default_pkg
from delete_proj import delete_proj
from new_proj import new_proj
from switch_proj import switch_proj

from proj_helper import proj_helper, ProjectNameError

blank_profile = 'example_profile_blank'
test_profile = 'test_profile'

def run_test():
   copyfile( blank_profile, test_profile )

   ph = proj_helper( test_profile )

   proj_name_1 = 'Proj_Test_1'
   proj_name_2 = 'Proj_Test_2'

   pkg_name_1 = 'Pkg_Test_1'
   pkg_name_2 = 'Pkg_Test_2'

   proj_type_1 = 'Type_1'
   proj_type_2 = 'Type_2'

   # NEW_PROJ test

   # no default, empty package name, empty type
   proj_name = proj_name_1
   pkg_name = ''
   proj_type = ''
   ph.read_profile()
   assert proj_name not in ph.projects
   new_proj( proj_name, pkg_name, proj_type, False, profile=test_profile )
   ph.read_profile()
   assert proj_name in ph.projects
   assert proj_name != ph.default_project
   assert ( pkg_name, proj_type ) == ph.projects[ proj_name ]

   # default, with package name
   proj_name = proj_name_2
   pkg_name = pkg_name_2
   proj_type = proj_type_2
   ph.read_profile()
   assert proj_name not in ph.projects
   new_proj( proj_name, pkg_name, proj_type, True, profile=test_profile )
   ph.read_profile()
   assert proj_name in ph.projects
   assert proj_name == ph.default_project
   assert ( pkg_name, proj_type ) == ph.projects[ proj_name ]


   # DELETE_PROJ test
   
   # delete non-default project
   proj_name = proj_name_1
   ph.read_profile()
   assert proj_name in ph.projects
   assert proj_name != ph.default_project
   delete_proj( proj_name, profile=test_profile )
   ph.read_profile()
   assert proj_name not in ph.projects
   # re-add proj for rest of tests
   new_proj( proj_name_1, pkg_name_1, proj_type_1, True, profile=test_profile )
   
   # delete default project, verify top project is now default
   proj_name = proj_name_2
   ph.read_profile()
   assert proj_name in ph.projects
   assert proj_name != ph.default_project
   delete_proj( proj_name, profile=test_profile )
   ph.read_profile()
   assert proj_name not in ph.projects
   assert proj_name != ph.default_project
   top_project = ph.projects.keys()[ 0 ]
   assert top_project == ph.default_project
   # re-add proj for rest of tests
   new_proj( proj_name_2, pkg_name_2, proj_type_2, True, profile=test_profile )


   # SWITCH_PROJ test

   # switch to non-default project
   proj_name = proj_name_1
   ph.read_profile()
   assert proj_name != ph.default_project
   switch_proj( proj_name, profile=test_profile )
   ph.read_profile()
   assert proj_name == ph.default_project


   # DEFAULT_PKG test

   # no project name (uses default project)
   proj_name = proj_name_1
   pkg_name_old = pkg_name_1
   pkg_name_new = pkg_name_2
   proj_type = proj_type_1
   ph.read_profile()
   assert ( pkg_name_old, proj_type ) == ph.projects[ proj_name ]
   default_pkg( pkg_name_new, proj_name, profile=test_profile )
   ph.read_profile()
   assert ( pkg_name_new, proj_type ) == ph.projects[ proj_name ]


   # GET_FULL_PROJECT_NAME test

   # setup for project name test
   fpn_exact = 'fpn_'
   fpn_a = 'fpn_a'
   fpn_b = 'fpn_b'
   fpn_full = 'fpn_unique_one'
   new_proj( fpn_exact, '', '', False, profile=test_profile )
   new_proj( fpn_a, '', '', False, profile=test_profile )
   new_proj( fpn_b, '', '', False, profile=test_profile )
   new_proj( fpn_full, '', '', False, profile=test_profile )
   fpn_ambiguous = 'fpn'
   fpn_sub = 'fpn_unique'
   fpn_none = 'fpn_none'
   ph.read_profile()
   projects = ph.projects

   # exact match
   assert fpn_a == ph.get_full_project_name( fpn_a )

   # substring match
   assert fpn_full == ph.get_full_project_name( fpn_sub )

   # no matches
   try:
      ph.get_full_project_name( fpn_none )
   except ProjectNameError:
      pass
   else:
      assert False

   # multiple matches
   try:
      ph.get_full_project_name( fpn_ambiguous )
   except ProjectNameError:
      pass
   else:
      assert False

   # exact match with multiple substring match
   assert fpn_exact == ph.get_full_project_name( fpn_exact )


   # BLANK PROFILE test
   # test to make sure that all functions behave properly even with a blank profile

   def check_empty_profile():
      ph.read_profile()
      assert ph.default_project == ''
      assert ph.projects == {}

   copyfile( blank_profile, test_profile )
   check_empty_profile()
   
   # new_proj blank test copyfile( blank_profile, test_profile )
   copyfile( blank_profile, test_profile )
   new_proj( proj_name_1, pkg_name_1, proj_type_1, True, profile=test_profile )
   ph.read_profile()
   assert ph.projects == { proj_name_1: ( pkg_name_1, proj_type_1 ) }
   assert ph.default_project == proj_name_1

   # delete_proj deleting last project test
   delete_proj( proj_name_1, profile=test_profile )
   check_empty_profile()

   # delete_proj blank test
   copyfile( blank_profile, test_profile )
   try:
      delete_proj( proj_name_1, profile=test_profile )
   except ProjectNameError:
      pass
   else:
      assert False
   check_empty_profile()

   # switch_proj blank test
   copyfile( blank_profile, test_profile )
   try:
      switch_proj( proj_name_1, profile=test_profile )
   except ProjectNameError:
      pass
   else:
      assert False
   check_empty_profile()

   # default_pkg blank test
   copyfile( blank_profile, test_profile )
   try:
      default_pkg( pkg_name_1, proj_name_1, profile=test_profile )
   except ProjectNameError:
      pass
   else:
      assert False
   check_empty_profile()

   # get_full_project_name blank test
   copyfile( blank_profile, test_profile )
   try:
      ph.get_full_project_name( proj_name_1 )
   except ProjectNameError:
      pass
   else:
      assert False
   check_empty_profile()

   os.remove( test_profile )

if __name__ == '__main__':
   run_test()
   print "TEST PASSED"

