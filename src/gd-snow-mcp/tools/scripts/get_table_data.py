import os
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow, table
from gd_servicenow_api import incident_state
load_dotenv()
servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")
service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)
result = service_now_client.get_table_with_offset(table='incident', sys_id = '', name = '', rows = 1, name_override = '', offset=0, extra_params= '' )
print(result)