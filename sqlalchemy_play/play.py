import logging

import sqlalchemy

from sqlalchemy import create_engine, Engine, text, URL
from sqlalchemy.exc import ProgrammingError

LOGGER = logging.getLogger(__name__)


class Play:
    url_object: URL
    engine: Engine

    def __init__(self):
        # Check sqlalchemy is installed and what version it's on;
        LOGGER.info(f"SQLAlechemy version: {sqlalchemy.__version__}")

        # Generate the db connection url;
        url_object: URL = URL.create(
            "postgresql+psycopg2",
            username="play",
            password="play",  # plain (unescaped) text
            host="localhost",
            database="play",
            port=5439,  # Note my non-standard port number 5439
        )
        LOGGER.info(f"DB connection url = {url_object}")

        ### Engine
        # Create an engine that can connect to the DB. NB: Rather than URL, can just put the text
        # string here if it's easier than using URL.create()
        self.engine = create_engine(url_object)

    def run_all(self):
        self.connections()
        self.results()

    def connections(self):
        # Create a connection and execute a query;
        with self.engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            LOGGER.info(result.all())

        ## connect() - "commit as you go" style
        # Using connect(), when a connection goes out of scope, a DB ROLLBACK is called. So, need to
        # run conn.commit() if want to save anything
        # E.g. Create a table and add some content;
        with self.engine.connect() as conn:
            try:
                conn.execute(text("CREATE TABLE some_table (x int, y int)"))
            except ProgrammingError as e:
                if "psycopg2.errors.DuplicateTable" in e.args[0]:
                    LOGGER.info("Table already created. Ignoring")
                else:
                    raise e
            conn.commit()

        ## begin() - "begin once" style
        # Using begin(), when a connection goes out of scope the commit is made automatically.
        # This is more commonly used than the commit-as-you-go style using begin()
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


if __name__ == "__main__":
    play = Play()
    play.run_all()
