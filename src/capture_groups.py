#!/usr/bin/env python2
# Author: Jayden Navarro

# CAPTURE_GROUP: default_project
rgx_default_project = [ 'export CURR_WS=\"(.*)\"' ]
fmt_default_project = 'export CURR_WS=\"%s\"\n'

# CAPTURE_GROUP: projects
rgx_projects = [ r'\"\$CURR_WS\" == \"(.*)\"', 'export CURR_PK=\"(.*)\"',
                 'export CURR_TYPE=\"(.*)\"' ]
fmt_projects = '''\
if [ "$CURR_WS" == "%s" ]
then
    export CURR_PK="%s"
    export CURR_TYPE="%s"
fi
'''
