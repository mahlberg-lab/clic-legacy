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

    # NB: virtualenv package might be called python-virtualenv
    apt-get install virtualenv python-dev \
        subversion \
        postgresql libpq-dev \
        libxml2-dev libxslt1-dev \
        postgresql

Configure virtualenv::

    virtualenv .

Get some packages not available via. PyPI::

    ./bin/pip install http://www.panix.com/~asl2/software/PyZ3950/PyZ3950-2.04.tar.gz

    svn checkout svn://svn.code.sf.net/p/pywebsvcs/code/branches/v1_5 pywebsvcs-code
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

    # Create clic-dickens user & DB, configure CLiC with the password
    sudo -upostgres createuser -P clic-dickens
    sudo -upostgres createdb -O clic-dickens db_annotation
    echo "dbpassword-you-supplied-to-createuser" > secret-dbpassword.txt

    sudo -upostgres pg_restore --dbname=db_annotation --verbose postgres.db_annotation.dump

Untar the cheshire3 stores/indexes::

    tar -C dbs/dickens -jxf cheshire3.db_dickens.tar.bz2

Untar the textfiles::

    tar -C clic/textfiles/ -jxf textfiles.tar.bz2

Once the system is started you will want to populate the chapter cache pickle,
if not already populated. Visit ``/api/concordance-warm/`` and make a cup of tea.
After it is done restart the service to ensure all workers are using the cache.

Developing the system
---------------------

Start the webserver in debug mode::

    ./bin/python -m clic.web.index

Run some unit tests::

    ./bin/python -m pytest clic/tests/unit/

Production installation
-----------------------

On a production environment, we host CLiC with uwsgi with NGINX serving static
files and proxying. So if not already installed::

    apt-get install nginx

The ``install.sh`` script will install CLiC onto a production environment, and
should be run as root, e.g. ``sudo ./install.sh``. This will:

* Create a secretkey to use as a salt for cookie strings
* Configure systemd to launch the UWSGI process running CLiC, and start it
* Create / update an NGINX site config to use CLiC, and get NGINX to reload
  the config.

There a host of environment variables that can be customised, see the top of
the script. You can override them thus::

    sudo SERVER_NAME=clic-stage.bham.ac.uk  ./install.sh

If you need to stop/start CLiC outside this for whatever reason, use systemctl,
e.g. ``systemctl stop clic``.


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
