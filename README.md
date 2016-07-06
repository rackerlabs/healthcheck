# healthcheck

To run

If a database is set up, run the manage.py file with,
DEV_DATA"BASE_URL='postgresql://DB_username:DB_password@localhost:DB_port/DB_name' "  where DB_name is the
name of the database.
For instance: DEV_DATABASE_URL='postgresql://user234:password@localhost:5432/canaryDB' python manage.py

If there is no database set up, currently it will default to using
"sqlite:///' + os.path.join(basedir, 'data-dev.sqlite)"