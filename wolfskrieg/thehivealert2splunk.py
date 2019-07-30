#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, json, requests, datetime, time, splunk, thehive

#method to create epoch time based on hours
def createTime(hours=1):
    """
    Method to extract the time from hours ago.
    """
    return str(int(round(time.time() * 1000))-(hours*60*60*1000))
#intiate connection to both theHive and Splunk
hive=thehive.theHiveConnection
splunkec=splunk.EventCollector

for alert in hive.getAlert(time=createTime(hours=168)):
    alert['routing'] = alert['_routing']
    alert['parent'] = alert['_parent']
    splunkec.add_event(alert, 'alert')
    artifacts=alert['artifacts']
    for artifact in artifacts:
        artifact['alertId']=alert['id']
        splunkec.add_event(artifact, 'artifact')
        print(json.dumps(artifact, indent=4, sort_keys=True))
