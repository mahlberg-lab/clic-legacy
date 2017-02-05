Setup Instructions
==================

Firstly, install the operating system prerequisites::

    apt-get install virtualenv python-dev \
        postgresql-9.4 libpq-dev \
        libxml2-dev libxslt1-dev

Get packages that pip can't get at::

    # NB: It's not really a .tar.gz
    wget -O PyZ3950-2.04.tar http://www.panix.com/~asl2/software/PyZ3950/PyZ3950-2.04.tar.gz
    ./bin/pip install PyZ3950-2.04.tar

    svn checkout svn://svn.code.sf.net/p/pywebsvcs/branches/v1_5 pywebsvcs-code
    mv pywebsvcs-code/wstools pywebsvcs-code/zsi/ZSI/wstools/
    ./bin/pip install pywebsvcs-code/zsi/

Comment out "socket.setdefaulttimeout(30)" in

    lib/python2.7/site-packages/cheshire3/web/documentFactory.py

See https://github.com/coleifer/micawber/issues/59 for more information

Install the operating system's postgres. As the postgres user::

    # Clear out old DB if it exists
    dropdb db_annotation
    dropuser clic-dickens

    # Create clic-dickens user, hardcoded password is dickens
    sudo -u postgres createuser -P -d -r -s clic-dickens

    createdb -O clic-dickens db_annotation --password

    # db_annotation.tar is available on the project share
    pg_restore --dbname=db_annotation --verbose /clic-project/clic/db_annotation.tar

Add links so cheshire3 can find the config::
    
    ln -rs cheshire3-server ~/.cheshire3-server

Start the webserver in debug mode::

    PYTHONPATH="." ./bin/python -m clic.web.index

Run some unit tests::

    PYTHONPATH="." ./bin/py.test clic/tests/unit/test_concordance.py
