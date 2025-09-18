import os
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow
from gd_servicenow_api import incident_state
load_dotenv()
servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")
service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)
class IncidentStateChange:

    sys_id='72d34fe70f376650035745d800d1b2b8'
    result = service_now_client.incident_change_state(sys_id, incident_state.IncidentState.CANCELED)
