# sqlalchemy_play Notes

# Installation notes

- Created a basic python project using `grum_make_python_workspace -m sqlalchemy-play`
- Added `alembic` and `SQLAlchemy` to requirements.in
- ran

```bash
pip-compile requirements.in
pip-sync
```

- Added docker-compose.yml for postgres db
  - NB:
    - I set the port to 5439, rather than the default 5432
    - I overrode the admin user from postgres/postgres with play/play
    - DB content is preserved locally in ./db./pgdata, but is gitignored, so not version controlled

- After `docker-compose up`;
  - Can connect using `psql -hlocalhost -p5439 -dplay -Uplay`, with password `play`
  - Can also connect using Adminer using;
    - <localhost:8080>
    - System = PostgreSQL
    - Server = sqlalchemyplay <- This is the name set in docker-compose.yml
    - User = play
    - Password = play
    - Database = play
    - _(Doesn't seem to care we're not using the default port)_


