#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, json, requests, datetime, time, splunk, sentinelone

#intiate connection to both theHive and Splunk
s1c=sentinelone.SentinelOneConnection
splunkEC=splunk.EventCollector

#retrieve all case information from theHive
agents = s1c.getAgents()

#iterate through each case
for agent in agents:
    #change the caseId to caseNumber for more clarity
    #add the case as an event into splunk
    splunkEC.add_event(agent, 'agent')
