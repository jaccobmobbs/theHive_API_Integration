#!/usr/bin/env python3
# -*- coding: utf-8 -*

import json, requests

class SplunkEventCollector:
    """
        Python API for Splunk Event Collector

    """
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.host = ""

    def _post(self, event, type):
        """
            Private method to send POST requests and parse the Response
        """
        data={
            "host": self.host,
            "source" : "thehive",
            "event": event
        }

        if type=='artifact':
            data["sourcetype"]="thehive_artifact"

        if type=='case':
            data["sourcetype"]="thehive_case"

        if type=='alert':
            data["sourcetype"]="thehive_alert"

        if type=='agent':
            data["sourcetype"]="agents"

        return requests.post(url=self.url, headers=self.headers, json=data).text

    def add_event(self, event, type):
        self._post(event, type)
