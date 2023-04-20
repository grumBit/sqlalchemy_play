import logging

from sqlalchemy import Column, Engine, ForeignKey, Integer, MetaData, String, Table

from sqlalchemy_play import play_orm

LOGGER = logging.getLogger(__name__)

# Create shared metadata object
metadata_obj = MetaData()


class DBMetaData:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def get_user_account_table() -> Table:
        if "user_account_core_style" not in metadata_obj:
            # Define a user account table with 3 columns; id, nickname & fullname
            Table(
                "user_account_core_style",  #               Table name. Grum: Added _core_style suffix to have both style expamples
                metadata_obj,  #                            MetaData object to add table to. NB: tables can be in many.
                Column("id", Integer, primary_key=True),  # Note the primary key constraint being set
                Column("nickname", String(30)),
                Column("fullname", String),
            )
        return metadata_obj.tables["user_account_core_style"]

    @staticmethod
    def get_address_table() -> Table:
        if "address_core_style" not in metadata_obj:
            # Define an address table
            Table(
                "address_core_style",  # Grum: Added _core_style suffix to have both style expamples
                metadata_obj,
                Column("id", Integer, primary_key=True),
                Column(
                    "user_id",
                    ForeignKey("user_account_core_style.id"),
                    nullable=False,  # Grum: my _core_style suffix needed
                ),  # Note foreign key constraint to the user
                Column(
                    "email_address", String, nullable=False
                ),  # Note nullable constraint ~= SQL “NOT NULL” constraint
            )
        return metadata_obj.tables["address_core_style"]

    def setting_up_MetaData_with_Table_objects(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#setting-up-metadata-with-table-objects

        # Note: metadata_obj was created globally so it can be shared.

        # Define a user account table with 3 columns; id, nickname & fullname
        user_account_table = self.get_user_account_table()

        ### Table components https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#components-of-table
        # Columns can be accessed by name;
        LOGGER.info(user_account_table.columns.nickname.__repr__())
        LOGGER.info(user_account_table.c.nickname.__repr__())  # The magic of Table.c - a shorthand for Table.columns

        # Column names can be found;
        LOGGER.info(user_account_table.columns.keys())

        ### Defining constraints https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-simple-constraints
        # Table constraints can be found;
        LOGGER.info(user_account_table.primary_key)  # NB: If not set returns a default empty PrimaryKeyConstraint

        # Define an address table
        address_table = self.get_address_table()

        ### Emitting DDL to the Database
        # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#emitting-ddl-to-the-database

        # Create the tables that have been defined in the MetaData;
        metadata_obj.create_all(self.engine)

    def using_ORM_declarative_forms_to_define_Table_Metadata(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata

        LOGGER.info(
            f"My Base class established a declaritive base, the class has a Metadata (Base.metadata={play_orm.Base.metadata} and Registry (Base.registry={play_orm.Base.registry}"
        )

        # The Base.metadata is populated with tables for classes that inherit from my Base class
        # (i.e. User & Address). This means the tables can be created using MetaData.create_all()
        play_orm.Base.metadata.create_all(self.engine)

    def table_reflection(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#table-reflection

        new_metadata_obj = MetaData()
        # Go off to the DB and find the existing some_table;
        user_account_table = Table("user_account_core_style", new_metadata_obj, autoload_with=self.engine)
        LOGGER.info(
            f"Using reflection, created a Table object with it's columns; {user_account_table.columns.__str__()}"
        )
        LOGGER.info(
            f"Reflection also populated the new MetaData object with the table; new_metadata_obj.tables={new_metadata_obj.tables}"
        )

    def run_all(self):
        self.setting_up_MetaData_with_Table_objects()
        self.using_ORM_declarative_forms_to_define_Table_Metadata()
        self.table_reflection()
