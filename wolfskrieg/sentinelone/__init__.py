#!/usr/bin/env python3
# -*- coding: utf-8 -*
from .connector import SentinelOne
from .config import url, token

SentinelOneConnection=SentinelOne(config.url, config.token)
sentinelone_app = Blueprint("sentinelone", __name__)

@sentinelone_app.route('/agents',  methods=['GET'])
def agent():
    return json.dumps(SentinelOneConnection.getAgents())

@sentinelone_app.route('/threats',  methods=['GET'])
def threats():
   return json.dumps(SentinelOneConnection.getThreats())

@sentinelone_app.route('/ioc', methods=['GET'])
def ioc():
    return json.dumps(SentinelOneConnection.getIoc())

@sentinelone_app.route('/resolve',  methods=['GET'])
def resolve():
    return json.dumps(SentinelOneConnection.markResolved())

@sentinelone_app.route('/uninstallReject',  methods=['GET'])
def uninstall():
    return json.dumps(SentinelOneConnection.uninstallReject())
