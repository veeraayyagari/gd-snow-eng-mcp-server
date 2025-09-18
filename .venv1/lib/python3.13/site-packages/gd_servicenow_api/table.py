try:
    from gd_servicenow_api.database import Database
    from gd_servicenow_api.ci_entity import CIEntity
    from gd_servicenow_api.data_lake_database import DataLakeDatabase
    from gd_servicenow_api.public_cloud_account import PublicCloudAccount
    from gd_servicenow_api.exceptions import InvalidServiceNowRequest, InvalidTableName, TableAlreadyExists, InvalidPublicCloudAccount
except ModuleNotFoundError:
    from database import Database
    from ci_entity import CIEntity
    from data_lake_database import DataLakeDatabase
    from public_cloud_account import PublicCloudAccount
    from exceptions import InvalidServiceNowRequest, InvalidTableName, TableAlreadyExists, InvalidPublicCloudAccount
except ImportError:
    from database import Database
    from ci_entity import CIEntity
    from data_lake_database import DataLakeDatabase
    from public_cloud_account import PublicCloudAccount
    from exceptions import InvalidServiceNowRequest, InvalidTableName, TableAlreadyExists, InvalidPublicCloudAccount


class Table(CIEntity):
    TABLE_NAME = "u_cmdb_ci_database_table_instance"

    def __init__(self, record: dict):
        super().__init__(record)

    def __init__(
        self,
        record: dict,
        data_lake_database: DataLakeDatabase = None,
    ):
        super().__init__(record)
        self.data_lake_database = data_lake_database
        if data_lake_database:
            if "u_table_tier" in record:
                self.u_table_tier = record["u_table_tier"]
            self.db_type = Database.DATALAKE
        else:
            self.db_type = Database.REDSHIFT

    @staticmethod
    def from_cmdb_by_sysid(sys_id: str):
        row = CIEntity.record_from_cmdb(Table.TABLE_NAME, sys_id=sys_id)
        if row is None:
            print(f"WARNING1: Unable to get table with sysid {sys_id}")
            return None
        db_sys_id = row["u_database_instance"]["value"]
        try:
            db_row = CIEntity.record_from_cmdb(
                DataLakeDatabase.TABLE_NAME, sys_id=db_sys_id
            )
            db_type = Database.DATALAKE
        except InvalidServiceNowRequest as e1:
            raise e1
        if db_row.get("u_aws_account") is None:
            print("WARNING: database row does not have u_aws_account field")
            return None
        public_cloud_account = PublicCloudAccount.from_cmdb(
            sys_id=db_row["u_aws_account"]["value"]
        )
        if db_type == Database.DATALAKE:
            data_lake_database = DataLakeDatabase(
                db_row, public_cloud_account=public_cloud_account
            )
            return Table(row, data_lake_database=data_lake_database)


    @staticmethod
    def get_db(name: str, public_cloud_account: PublicCloudAccount):
        db = DataLakeDatabase.from_cmdb(
            name=name,
            public_cloud_account=public_cloud_account,
        )
        return db



    @staticmethod
    def get_table(            table_name: str,
            data_lake_database_sysid: str,
    ):
        row = CIEntity.record_from_cmdb_extra(
            Table.TABLE_NAME,
            name=table_name,
            extra_params={"u_database_instance": data_lake_database_sysid},
        )
        return row

    @staticmethod
    def create(
            table_name: str,
            short_description: str,
            db: DataLakeDatabase,
            u_table_tier: int = None,
    ):

        row = CIEntity.create(
            Table.TABLE_NAME,
            {
                "name": table_name,
                "short_description": short_description,
                "u_database_instance": db.sys_id,
                "u_table_tier": u_table_tier,
            },
        )
        return Table(row, data_lake_database=db)

    @staticmethod
    def from_cmdb(name: str, dbtype: Database):
        # format is "AWS A/C Number.<database name>.<table name>"
        # e.g. "123456789012.my_database.my_table"
        parts = name.split(".")
        if len(parts) != 3:
            raise InvalidTableName(name)
        account_number = parts[0]
        database_name = parts[1]
        table_name = parts[2]
        public_cloud_account = PublicCloudAccount.from_cmdb(name=account_number)
        if public_cloud_account is None:
            raise InvalidPublicCloudAccount(account_number)
        if dbtype.value == Database.DATALAKE.value:
            data_lake_database = DataLakeDatabase.from_cmdb(
                name=database_name, public_cloud_account=public_cloud_account
            )
            if data_lake_database is None:
                return None
            row = CIEntity.record_from_cmdb_extra(
                Table.TABLE_NAME,
                name=table_name,
                extra_params={"u_database_instance": data_lake_database.sys_id},
            )
            if row is None:
                return None
            return Table(row, data_lake_database=data_lake_database)