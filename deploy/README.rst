Deploying CLiC
==============

Installation
------------

Install uWSGI
'''''''''''''

1. Make sure you have ``pip``::

    sudo apt-get install python-pip

2. Use ``pip`` to install ``uwsgi``::

    sudo pip install uwsgi


Start the uWSGI Emperor Process
'''''''''''''''''''''''''''''''

::

    sudo uwsgi --ini /cheshire3/clic/deploy/uwsgi/emperor.ini


.. NOTE::

   You should probably figure out how to run the uWSGI Emperor service,
   as invoked using the previous command, at boot time.
