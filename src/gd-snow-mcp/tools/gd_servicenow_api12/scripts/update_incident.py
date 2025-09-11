import os
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow
load_dotenv()
servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")
service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)
sys_id = '294d6f5a0fc60a40609b6798b1050e0e'
assignment_group_name = 'ENG-Servicenow'
result = service_now_client.assign_incident_to(sys_id, assignment_group_name)
print(result)
