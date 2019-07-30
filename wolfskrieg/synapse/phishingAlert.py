#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys, json
import logging, time, datetime
import eml_parser
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = current_dir + '/..'
sys.path.insert(0, current_dir)

from common.common import getConf
from objects.EwsConnector import EwsConnector
from objects.TheHiveConnector import TheHiveConnector
from objects.TempAttachment import TempAttachment
#import msg_parser

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

def phishingAlert():
    report = dict()
    report['success'] = bool()
    tempAttachment=None
    cfg = getConf()
    ewsConnector = EwsConnector(cfg)
    folder_name = cfg.get('EWS', 'folder_name')
    unread = ewsConnector.scan(folder_name)
    theHiveConnector = TheHiveConnector(cfg)
    for email in unread:
        conversationId = email.conversation_id.id
        alertTitle = str(email.subject)
        alertDescription = ('```\n' +
            'Alert created by Synapse\n' +
            'conversation_id: "' +
            str(email.conversation_id.id) +
            '"\n' +
            '```')
        alertArtifacts=[]
        alertTags=['CAT 7']
        for msg in email.attachments:
            try:
                #print(type(msg))
                q = dict()
                q['sourceRef'] = str(conversationId)
                esAlertId = theHiveConnector.findAlert(q)
                tempAttachment = TempAttachment(msg)
                if not tempAttachment.isInline:
                    #print('here')
                    tmpFilepath = tempAttachment.writeFile()
                    with open(tmpFilepath, 'rb') as fhdl:
                        raw_email = fhdl.read()
                        parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)
                    #print(parsed_eml['header']['header']['to'])
                        #print(json.dumps(parsed_eml, default=json_serial, indent=4, sort_keys=True))
                    alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='file', message="Phishing Email", data=tmpFilepath, tags=['Synapse']))
                    alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='other', message="Message Id", data=parsed_eml['header']['header']['message-id'][0], tags=['Synapse']))
                    for i in parsed_eml['header']['received_ip']:
                        alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='ip', message="Source IP", data=i, tags=['Synapse']))
                    alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='mail_subject', message="Phishing Email Subject", data=parsed_eml['header']['subject'], tags=['Synapse']))
                    for i in parsed_eml['header']['to']:
                        alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='mail', message="Recipients", data=i, tags=['Synapse']))
                    for i in parsed_eml['header']['header']['return-path']:
                        alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='mail', message="Return Path", data=i, tags=['Synapse']))
                    if 'x-originating-ip' in parsed_eml['header']['header']:
                        alertArtifacts.append(theHiveConnector.craftAlertArtifact(dataType='mail', message="Origin IP", data=parsed_eml['header']['header']['x-originating-ip'], tags=['Synapse']))
                    alert = theHiveConnector.craftAlert(alertTitle, alertDescription, severity=2, tlp=2, status="New", date=(int(time.time()*1000)), tags=alertTags, type="Phishing", source="Phishing Mailbox", sourceRef=email.conversation_id.id, artifacts=alertArtifacts, caseTemplate="Category 7 - Phishing")
                    theHiveEsAlertId = theHiveConnector.createAlert(alert)['id']


            except Exception as e:
                #msg_obj = msg_parser.msg_parser.Message(msg)
                #print(msg_obj.get_message_as_json())
                #msg_properties_dict = msg_obj.get_properties()
                print('Failed to create alert from attachment')

        readMsg = ewsConnector.markAsRead(email)

        #readMsg = ewsConnector.markAsRead(msg)



if __name__ == '__main__':
    phishingAlert()
