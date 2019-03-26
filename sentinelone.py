import json, requests, time

 

class SentinelOne:
    """
        Python API for SentinelOne
    """
    def __init__(self):

        self.url = '######'
        self.headers = {'content-Type': 'application/json', 'Authorization': 'APIToken ########'}
        self.session = session=requests.Session()

    def _send(self, request=''):

        response = self.session.get(self.url+request, headers=self.headers).text
        return json.loads(response)
 
    def getAgents(self, type='json'):
        """
            :param type: the string to define the returning result ('json' or 'datatable')
            :return: The JSON file of all agents in the cloud console
            :rtype: json file
        """
		
        json_data = self._send(request='/agents/iterator?limit=2000')
        s1_data = json_data['data']
        s1_last_id = json_data['last_id']
        
 
        #begin while loop to write json files to text file and loop until no more agents
        while(s1_last_id):
            json_data = self._send(request='/agents/iterator?limit=2000&last_id='+s1_last_id)
            s1_data = pandas.DataFrame(json_data['data'])
            s1_last_id =json_data['last_id']
            
        data_frame=data_frame.reset_index()
        if type=='datatable':
            return data_frame
        return data_frame.to_json()
 
    def getAlertThreats(self, days=1):
        """
            :param days: integer value for number of days
            :return: The JSON file of all threats in the cloud console
            :rtype: json file
        """
        time_frame = (days*24*60*60*1000)
        now = int(round(time.time() * 1000))
        diff = now-time_frame
        json_return=self._send(request='/threats?mitigation_status=1&created_at__gt='+str(diff))
        return json_return

    def getThreat(self, id=''):
        """
            :param id: string value of unique threat identifier
            :return: The JSON file of all threats in the cloud console
            :rtype: json file
        """
		
        json_return=self._send(request='/threats/'+id)
        return json_return
