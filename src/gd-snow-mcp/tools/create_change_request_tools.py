import os

from docutils.nodes import table
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow
load_dotenv()
servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")
service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)
class CreateChangeRequest:
    data = {
            "short_description": "testing change from new api",
            "description": "testing hgajiogj uhriwe eiru5392u ",
            "u_approval_group": "user-insights-platform",
            "assignment_group": "user-insights-platform",
            "backout_plan": "testing plan",
            "assigned_to": "sbhardwaj@godaddy.com",
            "u_jira_url": "https://godaddy-corp.atlassian.net/browse/ODP-486",
            "change_plan": "testing for deployment",
            "start_date": "2024-10-10 10:00:00",
            'u_critical_service_affected': 'Accounting',
            'risk': '4',
            'impact': '4',
            'end_date': "2024-10-31 12:00:00",
            'test_plan': "this is test plan"
        }
    result = service_now_client.create_change_request(data)
    print(result)
