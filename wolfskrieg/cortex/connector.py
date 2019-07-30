#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys, json, requests, datetime, time

class CortexConnector:
    """
        Python API for Cortex

    """
    def __init__(self, url, headers, post_header):

        self.url = url
        self.headers = headers
        self.post_header = post_header

    def _get(self, type, query=''):
        """
            Private method to send GET requests and parse the Response
        """
        if type=='job':
            request = self.url+'job/'+query
            #response = requests.get(self.url+'job/'query, headers=self.headers).text

        if type=='analyzer':
            request = self.url+'job/_search'+query

        return json.loads(requests.get(request, headers=self.headers).text)

    def _post(self, type, id, file payload):
        """
            Private method to send POST requests and parse the Response
        """
        if type=='analyzer':
            request = self.url+'analyzer/'+id+'/run/'

        return json.loads(requests.get(request, headers=self.headers, data=payload, files=file).text)

    def getJob(self, jobId):
        """
            :param id: String value of unique job identified
            :return: The JSON file of either the full report or the observables produced by an Analyzer job
            :rtype: json file
        """
        report = self._get('job', query=jobId)
        return report

#FIXME: run job for file attachments. #20190604 #runJob
    def runJob(self, analyzerId, file=None, **kwargs):
        payload = json.dumps(kwargs)
        files = { 'file' : ('tmpFile', open(file,'rb'), {'_json':'application/json'})}
        print(files['file'])
        report=self._post("analyzer", analyzerId, json.dumps(file), payload)
        return report

# TODO: Implements Cortex API functionality. #20190425 #API
