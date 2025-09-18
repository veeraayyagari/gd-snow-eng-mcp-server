from __future__ import annotations
from datetime import datetime
try:
    from gd_servicenow_api.exceptions import InvalidServiceNowRequest
except ModuleNotFoundError:
    from exceptions import InvalidServiceNowRequest


from typing import Protocol, Optional, Tuple, Dict, Any

class ObservabilityClient(Protocol):
    # returns (json_or_resp, headers, status_code)
    def get_table(
        self,
        table: str,
        sys_id: str | None = None,
        name: str | None = None,
        rows: int = 1,
        name_override: str | None = None,
        offset: int = 0,
        extra_params: str | None = None,
    ) -> tuple[dict | Any, dict, int]: ...

    # returns ({"result": [...]}, status_code)
    def get_table_with_offset(
        self,
        table: str,
        sys_id: str | None = None,
        name: str | None = None,
        rows: int = 10000,
        name_override: str | None = None,
        offset: int = 0,
        extra_params: str | None = None,
    ) -> tuple[dict, int]: ...

    # returns (json_or_resp, status_code)
    def get_table_dict(
        self,
        table: str,
        sys_id: str | None = None,
        name: str | None = None,
        rows: int = 1,
        name_override: str | None = None,
        offset: int = 0,
        extra_params_dict: dict | None = None,
    ) -> tuple[dict | Any, int]: ...

    # returns (json_or_resp, status_code)
    def table_write_op(self, table: str, record: dict, op: str) -> tuple[dict | Any, int]: ...

    # returns (json_or_resp, status_code)
    def table_write_op_by_sysid(self, table: str, sys_id: str, data: dict, method: str) -> tuple[dict | Any, int]: ...
class CIEntity:
    record_cache = dict()

    # Instantiate this at runtime using your secrets or env vars
    service_now_client: Optional[ObservabilityClient] = None



    def __init__(self, record: dict):
        self.name = record.get("name")
        self.short_description = record.get("short_description")
        self.sys_id = record.get("sys_id")
        self.sys_created_on = self._parse_date(record.get("sys_created_on"))
        self.sys_created_by = record.get("sys_created_by")
        self.sys_updated_on = self._parse_date(record.get("sys_updated_on"))
        self.sys_updated_by = record.get("sys_updated_by")

    @classmethod
    def configure(cls, client: ObservabilityClient) -> None:
        cls.service_now_client = client

    @classmethod
    def _client(cls) -> ObservabilityClient:
        if cls.service_now_client is None:
            raise RuntimeError(
                "CIEntity.service_now_client not configured. "
                "Call CIEntity.configure(ObservabilityServiceNow(...)) at startup."
            )
        return cls.service_now_client


    @staticmethod
    def _parse_date(date_str):
        if date_str:
            try:
                return datetime.strptime(date_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None
        return None

    @staticmethod
    def from_cmdb(table_name: str, name: str = None, sys_id: str = None):
        if not sys_id and not name:
            raise Exception("sys_id or name must be provided")
        response, headers, code = CIEntity._client().get_table(table_name, sys_id=sys_id, name=name)
        if code != 200:
            raise InvalidServiceNowRequest(response, code)
        result = response["result"]
        if isinstance(result, list):
            if len(result) == 0:
                return None
            result = result[0]
        return CIEntity(result)

    @staticmethod
    def record_from_cmdb(table_name: str, name: str = None, sys_id: str = None):
        key = f"{table_name}_{name}_{sys_id}"
        if key in CIEntity.record_cache:
            return CIEntity.record_cache[key]
        response, header, code = CIEntity._client().get_table(table_name, sys_id=sys_id, name=name)
        print(code)
        if code != 200:
            raise InvalidServiceNowRequest(response, code)
        result = response["result"]
        if isinstance(result, list):
            if not result:
                return None
            result = result[0]
        CIEntity.record_cache[key] = result
        return result

    @staticmethod
    def create(table_name: str, record: dict):
        response, code = CIEntity._client().table_write_op(table_name, record, "POST")
        if code != 201:
            raise InvalidServiceNowRequest(response, code)
        return response["result"]

    @staticmethod
    def update(table_name: str, sys_id: str, record: dict):
        response, code = CIEntity._client().table_write_op_by_sysid(table_name, sys_id, record, "PUT")
        if code != 200:
            raise InvalidServiceNowRequest(response, code)
        return response["result"]

    @staticmethod
    def delete(table_name: str, sys_id: str):
        response, code = CIEntity._client().table_write_op_by_sysid(table_name, sys_id, {}, "DELETE")
        if code != 204:
            raise InvalidServiceNowRequest(response, code)
        return {"status": "success", "message": f"Deleted sys_id {sys_id}"}

    @staticmethod
    def record_from_cmdb_extra(
            table_name: str, name: str = None, extra_params: dict = None
    ):
        cache_key = f"record_from_cmdb::{table_name}_{name}_{extra_params}"

        response, response_code = CIEntity._client().get_table_dict(
            table=table_name, name=name, rows=1, extra_params_dict=extra_params
        )
        if response_code != 200:
            raise InvalidServiceNowRequest(
                response=response, response_code=response_code
            )
        if len(response["result"]) == 0:
            return None
        row = response["result"][0]
        return row