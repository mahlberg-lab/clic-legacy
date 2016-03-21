Install the necessary python packages::

    pip install psycopg2 Flask-SQLAlchemy Flask-Migrate

This installs: SQLAlchemy, Flask-SQLAlchemy, Mako, alembic, Flask-Script, Flask-Migrate

Set up a postgres database::

    createdb --password annotation_dev
    ALTER USER jdejoode PASSWORD 'my_postgres_password';

