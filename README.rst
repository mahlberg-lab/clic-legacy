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
    sudo apt-get install virtualenv python-dev \
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

Use pip to fetch dependencies for the relevant environment (NB: this installs pandas, which can take an hour or so)::

    ./bin/pip install -r requirements.txt

Comment out "socket.setdefaulttimeout(30)" in

    lib/python2.7/site-packages/cheshire3/web/documentFactory.py

See https://github.com/coleifer/micawber/issues/59 for more information

Database setup
--------------

You need to pre-populate your CLiC instance. This requires the following files::

    postgres.db_annotation.dump
    cheshire3.db_dickens.tar.bz2
    textfiles.tar.bz2

These are available internally.

Configure the operating system's postgres. As the postgres user::

    # Generate a random password for python to use to access postgres
    dd if=/dev/random bs=20 count=1 | sha256sum | cut -f1 -d' ' > secret-dbpassword.txt

    # Create clic-dickens user & DB
    # This will ask for a password, give whatever is in secret-dbpassword.txt
    cat secret-dbpassword.txt
    sudo -upostgres createuser -P clic-dickens
    sudo -upostgres createdb -O clic-dickens db_annotation

    sudo -upostgres pg_restore --dbname=db_annotation --verbose postgres.db_annotation.dump

Untar the cheshire3 stores/indexes (NB: this will take some time)::

    tar -C dbs/dickens -jxf cheshire3.db_dickens.tar.bz2
    chmod o+w cheshire3-server/dbs/dickens/stores/*

Untar the textfiles::

    tar -C clic/textfiles/ -jxf textfiles.tar.bz2

Production installation
-----------------------

On a production environment, we host CLiC with uwsgi with NGINX serving static
files and proxying. So if not already installed::

    sudo apt-get install nginx

The ``install.sh`` script automates the following steps:

* Create a secretkey to use as a salt for cookie strings
* Ensure that the ``clic-chapter-cache.pickle`` is writable by the CLiC user
* Configure systemd to launch the UWSGI process running CLiC, and start it
* Create / update an NGINX site config to use CLiC, and get NGINX to reload
  the config.

There a host of environment variables that can be customised, see the top of
the script. Generally, the only one to override is SERVER_NAME, which controls
what DNS names the server will respond to. Multiple server names can be used,
separated by spaces.

For example, for installation on "clic-stage.bham.ac.uk"::

    sudo SERVER_NAME=clic-stage.bham.ac.uk  ./install.sh

Once this is done CLiC should be available for use. Next you want to ensure
that the cache is pre-warmed, see "Cache pre-warm".

If you need to stop/start CLiC outside this for whatever reason, use systemctl,
e.g. ``systemctl stop clic``.

Troubleshooting
---------------

If you cannot connect to CLiC from a web browser:

* Make sure you used a SERVER_NAME that matches the server
* Make sure NGINX started without errors: ``systemctl status -ln50 nginx``

If you see the "CLiC is down for maintenance" page:

* Make sure CLiC has started without errors: ``systemctl status -ln50 clic``

Cache pre-warm
--------------

For maximum performance, CLiC stores all chapters in memory. By default these are
read in as they are needed for concordance matches. This means that responses will
be very slow until all chapters have been looked at at least once.

To avoid this, you can force CLiC to read in every chapter in turn, so everything
is ready in memory, and dump this to ``clic-chapter-cache.pickle``, which will be
automatically read when CLiC restarts. To (re)generate this file do the following:
* Start CLiC, either in production or development
* Visit ``http://(server_name)/api/concordance-warm/``, make a cup of tea. You can use
  ``curl`` to run this command on the server to avoid network issues.
* Once it is finished, verify ``clic-chapter-cache.pickle`` exists and restart CLiC
  so all processes use the same cache file.

Back-up / generating dumps from live instances
----------------------------------------------

You can generate dumps from a running instance for backup / transfer::

    pg_dump -Fc db_annotation > postgres.db_annotation.dump
    tar -C dbs/dickens -jcvf cheshire3.db_dickens.tar.bz2 indexes stores
    tar -C clic/textfiles/ -jcvf textfiles.tar.bz2 .

User annotation system
----------------------

The registration system for new users  is currently disabled, so users need to be
added manually.

You can connect to the database as the ``clic-dickens`` user with the following::

    PGPASSWORD="$(cat secret-dbpassword.txt)" psql -h localhost -U 'clic-dickens' db_annotation

Then use the following SQL::

    INSERT INTO public.user
        (name, email, password, active, confirmed_at)
        VALUES
        ('NewUser', 'n.user@bham.ac.uk', 'plain-text-password', 't', NOW());

Developing the system
---------------------

To speed up development, pre-warm the cache as-per the "Cache pre-warm" section.

Start the webserver in debug mode::

    ./bin/python -m clic.web.index

Run some unit tests::

    ./bin/python -m pytest clic/tests/unit/

Acknowledgements
----------------

This work was supported by the Arts and Humanities Research Council grant reference AH/K005146/1
 
Please reference CLiC as the following:
 
Michaela Mahlberg, Peter Stockwell, Johan de Joode, Catherine Smith, Matthew Brook O’Donnell (forthcoming). “CLiC Dickens – Novel uses of concordances for the integration of corpus stylistics and cognitive poetics”, *Corpora*

This work is released under `AGPL-v3 <LICENSE.rst>`__.
