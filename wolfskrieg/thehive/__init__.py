#!/usr/bin/env python3
# -*- coding: utf-8 -*
#__init__ for theHive package
from .connector import theHiveConnector
from .config import url, token
from flask import Blueprint, request
import json

theHiveConnection=theHiveConnector(config.url, config.token)
thehive_app = Blueprint("thehive", __name__)

@thehive_app.route('/case',  methods=['GET'])
def case():
    caseid = request.args.get('id', None)
    return json.dumps(theHiveConnection.getCase(caseid))

@thehive_app.route('/alert',  methods=['GET'])
def alert():
   alertid = request.args.get('id', None)
   time = request.args.get('time', None)
   sourceRef = request.args.get('sourceRef', None)
   return json.dumps(theHiveConnection.getAlert(alertid, time, sourceRef))

@thehive_app.route('/', methods=['POST'])
def hivehook():
   data = json.loads(request.data)
   #TODO: setup webhook to send data received from theHive #20130730
   print(json.dumps(data, indent=4))
   return "OK"

@thehive_app.route('/artifact',  methods=['GET'])
def artifact():
    caseid = request.args.get('id', None)
    return json.dumps(theHiveConnection.getCaseArtifact(caseid))
