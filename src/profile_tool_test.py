#!/usr/bin/env python
# Author: Jayden Navarro

import filecmp
import os
from shutil import copyfile
import profile_tool as pt

orig_profile = 'example_profile'
test_profile = 'test_profile'

def runTest():
   copyfile( orig_profile, test_profile )

   ptool = pt.profile_tool( test_profile )

   # read groups, then write them back, confirm file doesn't
   # change
   groups = ptool.readGroups()
   ptool.writeGroups( groups )
   assert filecmp.cmp( orig_profile, test_profile )

   # confirm everything is as it should be from the file
   groups = ptool.readGroups()
   assert groups[ 'default_project' ] == [ ( 'Proj_A.0', ) ]
   assert groups[ 'projects' ] == [
      ( 'Proj_A.3', 'Pack_A/subdir', 'Type_A' ),
      ( 'Proj_B.4', 'Pack_B', 'Type_B' ),
      ( 'Proj_C.0', 'Pack_C', 'Type_C' ),
   ]

   os.remove( test_profile )

if __name__ == '__main__':
   runTest()
   print "TEST PASSED"
