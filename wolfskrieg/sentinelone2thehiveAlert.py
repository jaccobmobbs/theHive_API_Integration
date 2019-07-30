#!/usr/bin/env python3
# -*- coding: utf-8 -*
from markdownify import markdownify as md
import sys, json, requests, datetime, time, thehive, sentinelone

#initializing methods

def createTime(days=1):
    """
    Method to extract the time from days ago.
    """
    return (int(round(time.time() * 1000))-(days*24*60*60*1000))

def addAgentArtifact(agent, threat):
    """
    Method to extract artifacts from the threat and agent attributes to add to theHive
    """
    list=[]
    for ip in agent['networkInterfaces'][0]['inet']:
        list.append({'dataType': 'ip', 'data': ip, 'message': 'SentinelOne'})
    if threat['username']!="":
        list.append({'dataType': 'username', 'data': threat['username'], 'message': 'SentinelOne'})
    list.append({'dataType': 'hostname', 'data': agent['computerName'], 'message': 'SentinelOne'})
    if agent['domain']!="":
        list.append({'dataType': 'domain', 'data': agent['domain'], 'message': 'SentinelOne'})
    #os_info=agent['osName']+' '+agent['osArch']+' '+agent['osRevision']
    list.append({'dataType': 'os_info', 'data': agent['osType'], 'message': 'SentinelOne'})
    list.append({'dataType': 'hash', 'data': threat['fileContentHash'], 'message': 'SentinelOne'})
    if threat['fileDisplayName']!="":
        list.append({'dataType': 'filename', 'data': threat['fileDisplayName'], 'message': 'SentinelOne'})
    return list

def findIOC(iocs, list):
    description="\n***\nIndicators:"
    for id in list:
        for ioc in iocs:
            if id==ioc['id']:
                try:
                    des=md(ioc['description'])
                    description+="\n\t* "+des
                    break
                except:
                    description+="\n\t* "+ioc['description']
                    break
    return description

def sentinelone2thehiveAlert():
    instructions= ""
    #Initiating TheHive Api connection
    hive=thehive.theHiveConnection
    #Initiating SentinelOne connection
    s1c=sentinelone.SentinelOneConnection
    #Obtain all threats from the past 24 hours from SentinelOne
    threats=s1c.getThreats(mitigationStatuses="active", resolved=False, createdAt__gt=createTime())+s1c.getThreats(mitigationStatuses="suspicious", createdAt__gt=createTime())+s1c.getThreats(mitigationStatuses="mitigated", createdAt__gt=createTime())
    #get all indicators from sentinelone
    iocs=s1c.getIoc()
    #Now we iterate through the list of threats to create alerts for each
    for threat in threats:
        #grabbing the agent and indicator details
        agent=s1c.getAgents(ids=threat['agentId'])[0]
        indicators=findIOC(iocs, threat['indicators'])
        #setting up the tags
        tags=['CAT 3', threat['classification']]
        titleBegin = 'Active'
        severity=3
        if threat['mitigationStatus']=="active":
            severity=3
        elif threat['mitigationStatus']=="suspicious":
            titleBegin = 'Suspcious'
            severity=2
        elif threat['mitigationStatus']=="suspicious_resolved":
            titleBegin = 'Suspicious'
            severity=2
            tags.append("Resolved")
        elif threat['mitigationStatus']=="mitigated" and s1c.getReputation(threat['fileContentHash'])>5:
            titleBegin = 'Mitigated'
            severity=2
            tags.append("Resolved")
        else:
            severity=1
            tags.append("Resolved")
        #creating threat link, title, artifacts, and summary based on the threat details
        link="[Link](https://maximus.sentinelone.net/analyze/threats/"+str(threat['id'])+"/overview)"
        title='S1 '+titleBegin+' Threat - '+threat['fileDisplayName']+' on '+agent['computerName']
        artifacts=addAgentArtifact(agent, threat)
        summary = str('\n***\n' +
            '## Summary\n' +
            '|                         |               |\n' +
            '| ----------------------- | ------------- |\n' +
            '| **Link to Threat**      | ' + link + ' |\n' +
            '| **Site**                | ' + threat['siteName'] + ' |\n' +
            '| **Domain**              | ' + agent['domain'] + ' |\n' +
            '| **Group**               | ' + agent['groupName'] + ' |\n' +
            '| **Machine Name**        | ' + agent['computerName'] + ' |\n' +
            '| **Machine Type**        | ' + agent['machineType'] + ' |\n' +
            '| **Engine Detection**    | ' + str(threat['engines']) + ' |\n' +
            '| **Threat Kill**         | ' + str(threat['mitigationReport']['kill']['status']) + ' |\n' +
            '| **Threat Quarantine**   | ' + str(threat['mitigationReport']['quarantine']['status']) +' |\n***\n')
        #Creating an alert for theHive using the SentinelOne threat data
        response=hive.createAlert(
                                title=title,
                                tags=tags,
                                description=str(threat['description']+summary+indicators+instructions),
                                type='Malicious Code/Malware',
                                source='SentinelOne',
                                artifacts=artifacts,
                                sourceRef=threat['id'],
                                severity=severity
                                )
        return response.text
if __name__=='__main__':
    sentineloneAlert()
