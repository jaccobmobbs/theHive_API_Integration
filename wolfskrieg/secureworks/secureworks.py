#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, json, requests, datetime, time

    def __init__(self):
        self.url = ''
        self.headers = {'Content-Type': 'application/json', 'Authorization': ''}
        self.session = session=requests.Session()

    def _get(self, type, query=''):
        """
            Private method to send GET requests and parse the Response
        """
        if type == 'tickets':
            request = self.url+'/tickets/'+query
            response = json.loads(self.session.get(request, headers=self.headers).text)
            agents = self._iterate(request, response['data'], response['pagination']['nextCursor'])
            return agents

    def _post(self, type, payload):
        """
            Private method to send POST requests and parse the Response
        """
        if type == 'blacklist':
            request = self.url+'/threats/add-to-blacklist'
            response = self.session.post(request, headers=self.headers, data=payload).text
            return response

#TODO: Finish SecureWorks Reporting SDK #20190529 #SDK
#TODO: Create script for retrieving SecureWorks incidents every 15 minutes. #20190529 #Script
