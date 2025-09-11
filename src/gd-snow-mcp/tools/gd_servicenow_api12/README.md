# Observability Lib for ServiceNow

This is a Python Library to interact and manage the ServiceNow database

## Installation

```sh
pip install gd_servicenow_api12
```

## Usage

**Initialisation**

```sh
from gd_servicenow_api12 import observability_snow
service_now_client = observability_snow.ObservabilityServiceNow(username, password, client_id, client_secret, servicenow_api_url)
```
**Create Incident and update DNA form**

Example

```sh
incident = {
        "impact": 2,
        "priority": 3,
        "short_description": "[Test]Table SLA miss for sellbrite_cln.product_cln Tier 3",
        "correlation_display": "DnA Teams Intake",
        "made_sla": "false",
        "urgency": 2,
        "severity": 2,
        "category": "dna_incident",
        "u_issue_start": "2024-05-15 10:00:45",
        "description": "The table sellbrite_cln.product_cln missed its SLA. \nDetails:\nDatabase Name: sellbrite_cln\nTable Name: product_cln\nDelivery instance: {'year': '2024', 'month': '06', 'day': '06'}\nOriginal On-Call Group:DEV-Sellmore Horizontal",
        "assignment_group": "185ae321db8b409467eb5d30cf9619ab"
    }

dna_form =  {
        "impacted_data_set_tier": "tier3",
        "impact": 2,
        "data_producer_information": "dc-ucc-notifications",
        "email_address": "sellmore-horizontal@godaddy.com",
        "data_set_name": "sellbrite_cln.product_cln",
        "select_team": "commerce_data",
        "which_area_is_impacted": "Data Issue"
    }

cmdb_ci_id = {
    "name": "product_cln",
    "database": "sellbrite_cln",
    "db_class": "u_cmdb_ci_aws_data_lake"
}

payload = {
    'incident': incident,
    'dna_form': dna_form
}

result = service_now_client.create_incident_and_dna_form(payload.get("incident"), payload.get("dna_form"), 'DnA_Ops_Support_Group', cmdb_ci_id)
```

**Create Incident with CI (sys_id)**

```sh
message_json = {
        "impact": 2,
        "priority": 3,
        "short_description": "[Test]Table SLA miss for sellbrite_cln.product_cln Tier 3",
        "correlation_display": "DnA Teams Intake",
        "made_sla": "false",
        "urgency": 2,
        "severity": 2,
        "category": "dna_incident",
        "u_issue_start": "2024-05-15 10:00:45",
        "description": "The table sellbrite_cln.product_cln missed its SLA. \nDetails:\nDatabase Name: sellbrite_cln\nTable Name: product_cln\nDelivery instance: {'year': '2024', 'month': '06', 'day': '06'}\nOriginal On-Call Group:DEV-Sellmore Horizontal",
        "assignment_group": "185ae321db8b409467eb5d30cf9619ab"
    }

cmdb_ci_sys_id = "06c96b1fdbc81a10e804049ed3961915"

result = service_now_client.create_incident_with_ci(incident=message_json, assignment_group_name=None, cmdb_ci=cmdb_ci_sys_id)
```

**Get Incident**

```sh
result = service_now_client.get_incident(number="INCXXXXX")
```

**Incident State Change**

```sh
result = service_now_client.incident_change_state(sys_id, IncidentState.CANCELED)
```

**Assign Incident to team**

```sh
result = service_now_client.assign_incident_to(sys_id, assignment_group_name)
```

**Get table data**

```sh
result = service_now_client.get_table_with_offset(
            table: str, sys_id: str = None, name: str = None, rows: int = 10000, name_override: str = None, offset: int =0, extra_params: str = None
    )
```

**Get On-Call group details**

```sh
result = service_now_client.load_assignment_group(name="DnA_Ops_Support_Group")
```


## CMDB

***first step is to create Observability object and configure CIEntity***

```shell
    from gd_servicenow_api12.ci_entity import CIEntity
    
    obs = ObservabilityServiceNow(
            os.environ.get('SNOW_ARTIFACTORY_USERNAME_RW'), 
            os.environ.get('SNOW_ARTIFACTORY_PASSWORD_RW'),
            os.environ.get("SNOW_CLIENT_ID"),
            os.environ.get("SNOW_CLIENT_SECRET"), 
            os.environ.get("SNOW_API_URL")
        )
        CIEntity.configure(obs)
```

**Get public cloud account object**
```shell
from gd_servicenow_api12.public_cloud_account import PublicCloudAccount
public_cloud_uip = PublicCloudAccount.from_cmdb(name="account_id")
```

**Get RelationshipType object**
```shell
from gd_servicenow_api12.relationship_type import RelationshipType
relationship_type = CIRelationshipType.from_cmdb(name="Read by::Reads from")
```

**Get a table**
```shell
table = Table.get_table(table_name="table_name", data_lake_database_sysid="db_sys_id")
```

**Get a lake database**
```shell
db = Table.get_db(name="database_name", public_cloud_account=public_cloud_account_object)
```

**Get Data Processor Environment**
```shell
from gd_servicenow_api12.data_processor_environment import DataProcessorEnvironment
dp = DataProcessorEnvironment.from_cmdb(name="mwaa_env", public_cloud_account=public_cloud_account_object)
```


**Get Data Processor**
```sh
    from gd_servicenow_api12.data_processor import DataProcessor
    data_processor = DataProcessor.from_cmdb(name="dag_id", data_processor_environment=dp_env_object)
```

**Create a lake table**
```sh
    from gd_servicenow_api12.table import Table
    
    result = Table.create(table_name="table_name", short_description="testing purpose",
     db=DataLakeDatabase.from_cmdb(
                name="db_name",
                public_cloud_account=public_cloud_account_object,
            ), u_table_tier=3)
```




**Create a lake database**
```sh
    from gd_servicenow_api12.data_lake_database import DataLakeDatabase
    db = DataLakeDatabase.create(name="database_name", 
        short_description="short_description", public_cloud_account=public_cloud_account_object)
```

**Create a relationship**
```sh
  relationship = create_relationship(data_processor.sys_id, table.sys_id, relationship_type_object)
```

**Create a data processor/ airflow dag**
```sh
data_processor = service_now_client.create_snow_cmdb_processor_entry(
        dag_id="dag_id",
        data_processor_environment=dp_env_object,
        short_description="short_description"
    )
```