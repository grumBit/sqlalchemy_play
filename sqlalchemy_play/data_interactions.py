import logging

from sqlalchemy import Engine, insert, Insert, select, Table

LOGGER = logging.getLogger(__name__)


# https://docs.sqlalchemy.org/en/20/tutorial/data.html


class DataInteractions:
    engine: Engine
    user_table: Table
    address_table: Table

    def __init__(self, engine: Engine, user_table: Table, address_table: Table):
        self.engine = engine
        self.user_table = user_table
        self.address_table = address_table

    def _deep_alchemy_insert(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#the-insert-sql-expression-construct
        # This is here to add extra data for later examples.
        # It does some funky shstuff, so pretty much ignore!
        from sqlalchemy import select, bindparam

        scalar_subq = (
            select(self.user_table.c.id).where(self.user_table.c.nickname == bindparam("username")).scalar_subquery()
        )

        try:
            with self.engine.begin() as conn:
                result = conn.execute(
                    insert(self.address_table).values(user_id=scalar_subq),
                    [
                        {"username": "spongebob", "email_address": "spongebob@sqlalchemy.org"},
                        {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                        {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
                    ],
                )
        except Exception as e:
            if "more than one row returned by a subquery" in e.__str__():
                LOGGER.info(f"Must be running play twice as data already exists. Ignoring.")
            else:
                raise e

    def insert_sql_construct(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#the-insert-sql-expression-construct

        # Create an Insert statement. Note the parameterised fields passed in using .values();
        stmt: Insert = insert(self.user_table).values(nickname="spongebob", fullname="Spongebob Squarepants")
        LOGGER.info(f"insert statement: {stmt}")
        compiler = stmt.compile()
        LOGGER.info(f"The insert statement has params: {compiler.params}")

        # Execute the statement;
        with self.engine.begin() as conn:
            result = conn.execute(stmt)

        LOGGER.info(f"The inserted row has a primary key tuple: {result.inserted_primary_key}")

        # This time, instead of adding the params to the insert, pass in a list to the execute(), which
        # combines them as values with the insert
        list_of_params = [
            {"nickname": "sandy", "fullname": "Sandy Cheeks"},
            {"nickname": "patrick", "fullname": "Patrick Star"},
        ]
        with self.engine.begin() as conn:
            result = conn.execute(insert(self.user_table), list_of_params)

        # Add some extra rows for later examples
        self._deep_alchemy_insert()

        # INSERT...RETURNING
        insert_stmt = insert(self.address_table).returning(self.address_table.c.id, self.address_table.c.email_address)
        LOGGER.info(f"Can add return of specific columns; {insert_stmt}")

        # INSERT...FROM SELECT
        # This would generate an aol email address for all users;
        select_stmt = select(self.user_table.c.id, self.user_table.c.nickname + "@aol.com")
        insert_stmt = insert(self.address_table).from_select(["user_id", "email_address"], select_stmt)
        LOGGER.info(f"Can use data from a select to generate an insert: {insert_stmt}")

        # Combining FROM SELECT and RETURNING
        select_stmt = select(self.user_table.c.id, self.user_table.c.nickname + "@aol.com")
        insert_stmt = insert(self.address_table).from_select(["user_id", "email_address"], select_stmt)
        LOGGER.info(
            f"Can combine FROM SELECT and RETURNING:  {insert_stmt.returning(self.address_table.c.id, self.address_table.c.email_address)}"
        )

    def select_sql_construct(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#using-select-statements
        pass

    def run_all(self):
        self.insert_sql_construct()
        self.select_sql_construct()
