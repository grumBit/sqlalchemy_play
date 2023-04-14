import logging

from sqlalchemy import Engine, insert, Insert, select, Table
from sqlalchemy.orm import Session

from sqlalchemy_play.play_orm import User

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

    def insert_using_orm(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-inserting-orm

        squidward = User(name="squidward", fullname="Squidward Tentacles")
        krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

        LOGGER.info(f"We now have some User objects; {squidward}, {krabs}")
        with Session(self.engine) as session:
            session.add(squidward)
            session.add(krabs)
            LOGGER.info(f"The added Users are 'new': {session.new}")
            session.commit()
            LOGGER.info(f"Having commited, the Users are no longer 'new': {session.new}")

    def select_sql_construct(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#using-select-statements

        # Create a select statement;
        stmt = select(self.user_table).where(self.user_table.c.nickname == "spongebob")
        LOGGER.info(f'select(self.user_table).where(self.user_table.c.nickname == "spongebob") becomes; {stmt}')

        # Iterating through returned results, which returns rows;
        with self.engine.connect() as conn:
            for row in conn.execute(stmt):
                LOGGER.info(f"Iterating through returned ROWS; {row}")

        # Doing the same thing using ORM, which returns User entities (not rows)
        stmt = select(User).where(User.name == "squidward")
        LOGGER.info(f'select(User).where(User.name == "squidward") becomes; {stmt}')
        with Session(self.engine) as session:
            for user in session.execute(stmt):
                LOGGER.info(f"Iterating through returned User entities; {user}")

        # Create a select with limited columns;
        LOGGER.info(
            f"Select just the nickname and fullname (note the FROM is inferred); {select(self.user_table.c.nickname, self.user_table.c.fullname)}"
        )

        # Doing the same thing using a tuples;
        LOGGER.info(f"Select nickname and fullname using a tuples; {select(self.user_table.c['nickname', 'fullname'])}")

        # When specifying the columns using the ORM, we now get back rows, NOT User entities;
        LOGGER.info(
            f"Select just the name using the ORM; {session.execute(select(User.id, User.name, User.fullname, User.fullname)).first()}"
        )

        # Even when all columns are specified, rows are returned, NOT User entities;
        LOGGER.info(
            f"Even when all columns are specified, rows are returned; {session.execute(select(User.id, User.name, User.fullname, User.fullname)).first()}"
        )

        # GRUM: There is a lot more that can be done with ordering, joining, grouping etc, but I paused at this point;
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#selecting-orm-entities-and-columns

    def run_all(self):
        self.insert_sql_construct()
        self.insert_using_orm()
        self.select_sql_construct()
