try:
    from gd_servicenow_api.ci_entity import CIEntity
    from gd_servicenow_api.exceptions import DataProcessorEnvironmentAlreadyExists
    from gd_servicenow_api.public_cloud_account import PublicCloudAccount
except ModuleNotFoundError:
    from ci_entity import CIEntity
    from exceptions import DataProcessorEnvironmentAlreadyExists
    from public_cloud_account import PublicCloudAccount
except ImportError:
    from ci_entity import CIEntity
    from exceptions import DataProcessorEnvironmentAlreadyExists
    from public_cloud_account import PublicCloudAccount


class DataProcessorEnvironment(CIEntity):
    TABLE_NAME = "u_cmdb_ci_data_processor_environment"

    # def __init__(self, name, short_description, sys_id):
    #     super().__init__(name, short_description, sys_id)

    def __init__(self, record: dict, public_cloud_account: PublicCloudAccount = None):
        super().__init__(record)

        if public_cloud_account is None:
            self.public_cloud_account = PublicCloudAccount.from_cmdb(
                sys_id=record["u_aws_account"]["value"]
            )
        else:
            self.public_cloud_account = public_cloud_account

    @staticmethod
    def from_cmdb(
        name: str = None,
        sys_id: str = None,
        public_cloud_account: PublicCloudAccount = None,
    ):
        if sys_id is None and (name is None or public_cloud_account is None):
            raise Exception(
                "sys_id or (name and public_cloud_account) must be provided"
            )
        if sys_id:
            row = CIEntity.record_from_cmdb(
                DataProcessorEnvironment.TABLE_NAME, sys_id=sys_id
            )
        else:
            row = CIEntity.record_from_cmdb_extra(
                DataProcessorEnvironment.TABLE_NAME,
                name=name,
                extra_params={"u_aws_account": public_cloud_account.sys_id},
            )
        if row is None:
            return None
        return DataProcessorEnvironment(row, public_cloud_account=public_cloud_account)

    @staticmethod
    def create(
        name: str, short_description: str, public_cloud_account: PublicCloudAccount
    ):
        existing = None
        try:
            existing = DataProcessorEnvironment.from_cmdb(
                name=name, public_cloud_account=public_cloud_account
            )
        except Exception as e:
            print(e)
        if existing is not None:
            raise DataProcessorEnvironmentAlreadyExists(name)
        row = CIEntity.create(
            DataProcessorEnvironment.TABLE_NAME,
            {
                "name": name,
                "short_description": short_description,
                "u_aws_account": public_cloud_account.sys_id,
            },
        )
        if row is None:
            return None
        return DataProcessorEnvironment(row, public_cloud_account=public_cloud_account)