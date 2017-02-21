CLiC: A corpus tool to support the analysis of literary texts
=============================================================

The CLiC Dickens project demonstrates through corpus stylistics how computer-assisted methods can be used to study literary texts and lead to new insights into how readers perceive fictional characters. As part of the project we are developing the web app CLiC, designed specifically for the analysis of literary texts. CLiC Dickens started at the University of Nottingham in 2013, it is now a collaborative project with the University of Birmingham. 

For more information, cf.
`CLiC Dickens - University of Nottingham
<http://www.nottingham.ac.uk/research/groups/cral/projects/clic.aspx/>`_ and `CLiC Dickens - University of Birmingham
<http://www.birmingham.ac.uk/schools/edacs/departments/englishlanguage/research/projects/clic.aspx/>`_. 

Installation
------------

Firstly, install the operating system prerequisites::

    apt-get install virtualenv python-dev \
        postgresql-9.4 libpq-dev \
        libxml2-dev libxslt1-dev

Configure virtualenv::

    virtualenv .

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

Use pip to fetch dependencies for the relevant environment::

    ./bin/pip install -r requirements/dev.txt

Database setup
--------------

You need to pre-populate your CLiC instance. This requires the following files::

    postgres.db_annotation.dump
    cheshire3.db_dickens.tar.bz2
    textfiles.tar.bz2

These are available internally.

Configure the operating system's postgres. As the postgres user::

    # Clear out old DB if it exists
    dropdb db_annotation
    dropuser clic-dickens

    # Create clic-dickens user & DB, hardcoded password is dickens
    createuser -P -d -r -s clic-dickens
    createdb -O clic-dickens db_annotation --password

    # Restore DB, db_annotation.tar is available on the project share
    pg_restore --dbname=db_annotation --verbose /clic-project/clic/db_annotation.tar

Untar the cheshire3 stores/indexes, and symlink so cheshire3 can find the config::

    tar -C dbs/dickens -jxf cheshire3.db_dickens.tar.bz2
    # NB: If not running as the eventual CLiC user, change ~ accordingly
    ln -rs cheshire3-server ~/.cheshire3-server

Untar the textfiles::

    tar -C clic/textfiles/ -jxf textfiles.tar.bz2

Developing the system
---------------------

Start the webserver in debug mode::

    ./bin/python -m clic.web.index

Run some unit tests::

    ./bin/python -m pytest clic/tests/unit/

Back-up / generating dumps from live instances
----------------------------------------------

You can generate dumps from a running instance for backup / transfer::

    pg_dump -Fc db_annotation > postgres.db_annotation.dump
    tar -C dbs/dickens -jcvf cheshire3.db_dickens.tar.bz2 indexes stores
    tar -C clic/textfiles/ -jcvf textfiles.tar.bz2 .

Acknowledgements
----------------

This work was supported by the Arts and Humanities Research Council grant reference AH/K005146/1
 
Please reference CLiC as the following:
 
Michaela Mahlberg, Peter Stockwell, Johan de Joode, Catherine Smith, Matthew Brook O’Donnell (forthcoming). “CLiC Dickens – Novel uses of concordances for the integration of corpus stylistics and cognitive poetics”, *Corpora*

This work is released under `AGPL-v3 <LICENSE.rst>`__.
