
try:
    from gd_servicenow_api.ci_entity import CIEntity
except ModuleNotFoundError:
    from ci_entity import CIEntity
except ImportError:
    from ci_entity import CIEntity

class CIRelationshipType:
    TABLE_NAME = "cmdb_rel_type"

    def __init__(self, record: dict):
        self.name = record["name"]
        self.sys_id = record["sys_id"]

    @staticmethod
    def from_cmdb(name: str = None, sys_id: str = None):

        if not sys_id and not name:
            raise Exception("Provide either name or sys_id")
        row = CIEntity.record_from_cmdb(CIRelationshipType.TABLE_NAME, name, sys_id)
        if not row:
            return None
        return CIRelationshipType(row)

