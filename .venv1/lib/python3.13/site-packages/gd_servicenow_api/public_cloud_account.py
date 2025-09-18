#!/usr/bin/python
# coding: utf-8
try:
    from gd_servicenow_api.ci_entity import CIEntity
    from gd_servicenow_api.exceptions import InvalidPublicCloudAccount
except ModuleNotFoundError:
    from ci_entity import CIEntity
    from exceptions import InvalidPublicCloudAccount
except ImportError:
    from ci_entity import CIEntity
    from exceptions import InvalidPublicCloudAccount


class PublicCloudAccount(CIEntity):
    TABLE_NAME = "u_cmdb_pubc_account"

    # def __init__(self, name, short_description, sys_id):
    #     super().__init__(name, short_description, sys_id)

    def __init__(self, record: dict):
        super().__init__(record)
        self.operational_status = record["operational_status"]
        self.u_budget_id = record["u_budget_id"]
        self.u_realm = record["u_realm"]
        self.u_maintenance_status = record["u_maintenance_status"]
        self.u_sync_source = record["u_sync_source"]
        self.u_pubc_environment = record["u_pubc_environment"]
        self.u_pubc_account_type = record["u_pubc_account_type"]

    @staticmethod
    def from_cmdb(name: str = None, sys_id: str = None):
        if sys_id is None and name is None:
            raise InvalidPublicCloudAccount(name)
        row = CIEntity.record_from_cmdb(PublicCloudAccount.TABLE_NAME, name, sys_id)
        if row is None:
            return None
        return PublicCloudAccount(row)