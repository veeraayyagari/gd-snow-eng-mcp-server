try:
    from gd_servicenow_api.ci_entity import CIEntity
    from gd_servicenow_api.data_processor_environment import DataProcessorEnvironment
    from gd_servicenow_api.exceptions import DataProcessorAlreadyExists
except ModuleNotFoundError:
    from ci_entity import CIEntity
    from data_processor_environment import DataProcessorEnvironment
    from exceptions import DataProcessorAlreadyExists
except ImportError:
    from ci_entity import CIEntity
    from data_processor_environment import DataProcessorEnvironment
    from exceptions import DataProcessorAlreadyExists


class DataProcessor(CIEntity):
    TABLE_NAME = "u_cmdb_ci_data_processor"

    # def __init__(self, name, short_description, sys_id, environment):
    #     super().__init__(name, short_description, sys_id)
    #     if isinstance(environment, DataProcessorEnvironment):
    #         self.environment = environment
    #     else:
    #         raise TypeError(
    #             "environment must be an instance of DataProcessorEnvironment"
    #         )

    def __init__(self, record: dict):
        super().__init__(record)
        self.pipeline_id = record["u_pipeline_id"]
        self.pipeline_version = record["u_pipeline_version"]
        self.processor_type = record["u_processor_type"]

    def __init__(
        self, record: dict, data_processor_environment: DataProcessorEnvironment = None
    ):
        super().__init__(record)
        self.pipeline_id = record["u_pipeline_id"]
        self.pipeline_version = record["u_pipeline_version"]
        self.processor_type = record["u_processor_type"]
        self.data_processor_environment = data_processor_environment

    @staticmethod
    def from_cmdb(
        name: str = None,
        sys_id: str = None,
        data_processor_environment: DataProcessorEnvironment = None,
    ):
        if sys_id is None and (name is None or data_processor_environment is None):
            raise Exception(
                "sys_id or (name and data_processor_environment) must be provided"
            )
        if sys_id:
            row = CIEntity.record_from_cmdb(DataProcessor.TABLE_NAME, sys_id=sys_id)
        else:
            row = CIEntity.record_from_cmdb_extra(
                DataProcessor.TABLE_NAME,
                name=name,
                extra_params={
                    "u_data_processor_environment": data_processor_environment.sys_id
                },
            )
        if row is None:
            return None
        return DataProcessor(row)

    @staticmethod
    def create(
            name: str,
            short_description: str,
            pipeline_id: str,
            pipeline_version: str,
            processor_type: str,
            data_processor_environment: DataProcessorEnvironment,
    ):
        existing = DataProcessor.from_cmdb(
            name=name, data_processor_environment=data_processor_environment
        )
        if existing is not None:
            raise DataProcessorAlreadyExists(name)
        req = {
            "name": name,
            "short_description": short_description,
            "u_data_processor_environment": data_processor_environment.sys_id,
            "u_pipeline_id": pipeline_id,
            "u_pipeline_version": pipeline_version,
            "u_processor_type": processor_type,
        }
        row = CIEntity.create(DataProcessor.TABLE_NAME, req)
        if row is None:
            return None
        return DataProcessor(row, data_processor_environment=data_processor_environment)