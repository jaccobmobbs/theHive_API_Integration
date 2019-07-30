from flask import Flask, render_template, url_for, copy_current_request_context, Blueprint
from sentinelone2thehiveAlert import sentinelone2thehiveAlert
from synapse.phishingAlert import phishingAlert
from threading import Thread, Event
import requests, json, time, thehive, sentinelone

app = Flask(__name__,  template_folder="templates")

app.register_blueprint(thehive.thehive_app, url_prefix='/thehive')

app.register_blueprint(sentinelone.sentinelone_app, url_prefix='/sentinelone')


@app.route('/', methods=['GET'])
def home():
    return render_template('wolfskrieg.html')

@app.route('/malwareAlert', methods=['GET'])
def s1alert():
    return json.dumps(sentinelone2thehiveAlert())

@app.route('/phishingAlert', methods=['GET'])
def phish():
    return json.dumps(phishingAlert())


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

#TODO: Work out organizing SDKs into actual packages #20190719
