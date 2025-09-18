
import requests
#from docutils.parsers.rst.directives.misc import Class

class GetIncident:

    def get_incident(instance_url, username, password):
        api_endpoint = f"{instance_url}/api/now/table/incident?sys_id=294d6f5a0fc60a40609b6798b1050e0e"
        response = requests.get(api_endpoint, auth=(username, password))
        if response.status_code == 200:
            return response.json()['result']
        else:
            print(f"Error fetching incidents: {response.text}")
            return ''

#recent_incidents = GetIncident.get_incident('https://godaddydev2.service-now.com','mcp_server', 'mcp_server')
#print(recent_incidents)

