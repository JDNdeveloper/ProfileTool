#!/usr/bin/env python
# Author: Jayden Navarro

# CAPTURE_GROUP: default_project
rgx_default_project = [ 'export CURR_WS=\"(.*)\"' ]
fmt_default_project = 'export CURR_WS=\"%s\"\n'

# CAPTURE_GROUP: projects
rgx_projects = [ r'\"\$CURR_WS\" == \"(.*)\"', 'export CURR_PK=\"(.*)\"' ]
fmt_projects = '''\
if [ "$CURR_WS" == "%s" ]
then
    export CURR_PK="%s"
fi
'''
