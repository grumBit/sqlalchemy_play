import logging

import sqlalchemy

from sqlalchemy import create_engine, Engine, text, URL
from sqlalchemy.orm import Session

LOGGER = logging.getLogger(__name__)

# https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html


class DBAPITransactions:
    # url_object: URL
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def get_engine(
        drivername: str = "postgresql+psycopg2",
        username: str = "play",
        password: str = "play",  # plain (unescaped) text
        host: str = "localhost",
        database: str = "play",
        port: int = 5439,  # Note my non-standard port number 5439
    ) -> Engine:
        # Check sqlalchemy is installed and what version it's on;
        LOGGER.info(f"SQLAlechemy version: {sqlalchemy.__version__}")

        ### Generate the db connection url;
        url_object: URL = URL.create(drivername, username, password, host, port, database)
        LOGGER.info(f"DB connection url = {url_object}")

        ### Create an Engine
        # https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine
        # Create an engine that can connect to the DB. NB: Rather than URL, can just put the text
        # string here if it's easier than using URL.create()
        return create_engine(url_object)

    def connections(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#getting-a-connection

        # Create a connection and execute a query;
        with self.engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            LOGGER.info(result.all())

        ## connect() - "commit as you go" style
        # Using connect(), when a connection goes out of scope, a DB ROLLBACK is called. So, need to
        # run conn.commit() if want to save anything
        # E.g. Create a table and add some content;
        with self.engine.connect() as conn:
            if sqlalchemy.inspect(self.engine).has_table("some_table", schema="public"):
                # Grum: Just doing this so that I can re-run theses examples over and over
                LOGGER.warning("some_table already exists - dropping it")
                conn.execute(text("DROP TABLE some_table"))

            conn.execute(text("CREATE TABLE some_table (x int, y int)"))
            conn.commit()

        ## begin() - "begin once" style
        # Using begin(), when a connection goes out of scope the commit is made automatically.
        # This is more commonly used than the commit-as-you-go style using begin() as it more succinct
        # E.g. Add some more content;
        #       - note there are 2 execute()s
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
            )
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
            )

    def results(self):
        # https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#basics-of-statement-execution

        ## Result - represents an iterable object of result rows containing named tuples
        # The iterable rows contained named tuples, so can index
        # E.g. execute a fetch into a Result;
        with self.engine.connect() as conn:
            # Basic iteration
            result = conn.execute(text("SELECT x, y FROM some_table"))
            for row in result:
                LOGGER.info(f"Basic iteration; x: {row.x}  y: {row.y}")

            # Iteration combined with tuple assignment (Note this is positional, so tuple names are irrelevant)
            result = conn.execute(text("SELECT x, y FROM some_table"))
            for a, b in result:
                LOGGER.info(f"Tuple assignment; x: {a}  y: {b}")

            # Indexing into tuples
            result = conn.execute(text("select x, y from some_table"))
            for row in result:
                y = row[1]
                LOGGER.info(f"Indexing into tuples; y: {y}")

            # Tuple attribute names
            result = conn.execute(text("SELECT x, y FROM some_table"))
            for row in result:
                LOGGER.info(f"Tuple attribute names; x: {row.x}  y: {row.y}")

            # Mapping Access
            result = conn.execute(text("select x, y from some_table"))
            for dict_row in result.mappings():
                LOGGER.info(f'Mapping Access; x: {dict_row["x"]}, y: {dict_row["y"]}')

    def sending_parameters(self):
        ### qmark parameter substitution
        # https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#sending-parameters
        # Execute a select using the : notation for qmark parameter substitution. qmark is strongly recommended
        # to avoid SQL injection attacks when the data is untrusted.

        # Select rows where y > 2 using parameter substitution
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
            for row in result:
                LOGGER.info(f"x: {row.x}  y: {row.y}")

        # https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#sending-multiple-parameters
        # This style of execution is known as executemany, which bundles up many changes into a single DB call
        # executemany doesn’t support returning of result rows, even if the statement includes the RETURNING clause
        # with some exceptions - see link above

        with self.engine.connect() as conn:
            conn.execute(
                text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
            )
            conn.commit()

    def executing_with_an_ORM_Session(self):
        # Executing with an ORM Session
        # https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#executing-with-an-orm-session

        # The following is equivalent to what is done in self.send_parameters()
        # Note Session is a "commit as you go" style (like engine.connect()), so commits are required.

        with Session(self.engine) as session:
            result = session.execute(text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y"), {"y": 6})
            for row in result:
                LOGGER.info(f"x: {row.x}  y: {row.y}")

        with Session(self.engine) as session:
            result = session.execute(
                text("UPDATE some_table SET y=:y WHERE x=:x"),
                [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
            )
            session.commit()

    def run_all(self):
        self.connections()
        self.results()
        self.sending_parameters()
        self.executing_with_an_ORM_Session()
