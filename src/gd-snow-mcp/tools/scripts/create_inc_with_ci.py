import os
from dotenv import load_dotenv
from gd_servicenow_api import observability_snow
load_dotenv()
servicenow_api_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")
from gd_servicenow_api import observability_snow
service_now_client = observability_snow.ObservabilityServiceNow(username, password, 'e78a061f7cd346388b10be87a08a5a86', '7nsw$|SMZx', servicenow_api_url)

message_json = {
        "impact": 2,
        "priority": 3,
        "short_description": "[Test]Table SLA miss for"+'sellbrite'+"_cln.product_cln Tier 3",
        "correlation_display": "DnA Teams Intake",
        "made_sla": "false",
        "urgency": 2,
        "severity": 2,
        "category": "dna_incident",
        "u_issue_start": "2024-05-15 10:00:45",
        "description": "The table sellbrite_cln.product_cln missed its SLA. \nDetails:\nDatabase Name:"+ "sellbrite"+"_cln\nTable Name: product_cln\nDelivery instance: {'year': '2024', 'month': '06', 'day': '06'}\nOriginal On-Call Group:DEV-Sellmore Horizontal",
        "assignment_group": "185ae321db8b409467eb5d30cf9619ab"
    }

cmdb_ci_sys_id = "06c96b1fdbc81a10e804049ed3961915"

result = service_now_client.create_incident_with_ci(incident=message_json, assignment_group_name='', cmdb_ci=cmdb_ci_sys_id)
print(result)