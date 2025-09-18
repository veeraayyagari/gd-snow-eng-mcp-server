try:
    from gd_servicenow_api.ci_entity import CIEntity
    from gd_servicenow_api.ci_relationship_type import CIRelationshipType
    from gd_servicenow_api.exceptions import InvalidServiceNowRequest
except ModuleNotFoundError:
    from ci_entity import CIEntity
    from ci_relationship_type import CIRelationshipType
    from exceptions import InvalidServiceNowRequest
except ImportError:
    from ci_entity import CIEntity
    from ci_relationship_type import CIRelationshipType
    from exceptions import InvalidServiceNowRequest

from urllib.parse import quote_plus
class CIRelationship:
    TABLE_NAME = "cmdb_rel_ci"

    def __init__(self, record: dict):
        self.sys_id = record["sys_id"]
        self.parent = record["parent"]["value"]
        self.child = record["child"]["value"]
        self.relationship_type = record["type"]["value"]

    @staticmethod
    def create(parent_sys_id: str, relationship_type: CIRelationshipType, child_sys_id: str):
        req = {
            "parent": parent_sys_id,
            "child": child_sys_id,
            "type": relationship_type.sys_id,
        }
        row = CIEntity.create(CIRelationship.TABLE_NAME, req)
        return CIRelationship(row)

    def delete(self):
        return CIEntity.delete(CIRelationship.TABLE_NAME, self.sys_id)

    @staticmethod
    def search_from_cmdb(parent_sys_id: str = None, child_sys_id: str = None, relationship_type_sys_id:str = None):
        params = {}
        if parent_sys_id:
            params["parent"] = parent_sys_id
        if child_sys_id:
            params["child"] = child_sys_id
        if relationship_type_sys_id:
            params["type"] = relationship_type_sys_id

        response, code = CIEntity.service_now_client.get_table_dict(
            table=CIRelationship.TABLE_NAME, rows=1000, extra_params_dict=params
        )
        if code != 200:
            raise InvalidServiceNowRequest(response, code)
        return [CIRelationship(row) for row in response["result"]]
