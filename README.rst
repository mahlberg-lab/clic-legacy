CLiC Project
============

Cheshire3 databases and applications for the CLiC Project.


How to initiate the database
----------------------------

    cp config.xml.tmpl config.xml
    # change the paths in that file
    # delete the postgres db if you have not configured it properly
    # delete concStore from run.py

    cd clic/dbs/dickens
    cheshire3-register config.xml
    
    # copy the data to the folder
    cheshire3-load data
    
    # create the indexes
    python run.py -load
    python run.py -ntc

Debugging
---------

Commands to debug the setup include:

    ls ~/.cheshire3-server/configs/databases
    rm -r clic/dbs/dickens/indexes
    rm -r clic/dbs/dickens/stores
    rm -r /tmp/cache

Run
---

Start a web-server to make the interface available locally::

    sudo su -c "uwsgi --http :8080 --wsgi-file clic/dickens/web/flask/api.py --callable app" cheshire
    cdproject & cd clic & uwsgi --ini deploy/uwsgi/apps/index.ini &
