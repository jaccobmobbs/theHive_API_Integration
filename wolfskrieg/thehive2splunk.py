#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, json, requests, datetime, time, splunk, thehive

#intiate connection to both theHive and Splunk
hive=thehive.theHiveConnection
splunkec=splunk.eventCollector

#retrieve all case information from theHive
cases = hive.getCase()

#iterate through each case
for case in cases:
    #change the caseId to caseNumber for more clarity
    case['caseNumber'] = case.pop('caseId')
    case['routing'] = case['_routing']
    #add the case as an event into splunk
    splunkec.add_event(case, 'case')
    #add all the artifacts from the case into splunk
    for artifact in hive.getCaseArtifact(case['id']):
        artifact['routing'] = artifact['_routing']
        artifact['parent'] = artifact['_parent']
        splunkec.add_event(artifact, 'artifact')
