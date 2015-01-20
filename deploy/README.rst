Deploying CLiC
==============

Installation
------------

Install Apache2
'''''''''''''''

::

    sudo yum install httpd


Install uWSGI
'''''''''''''

1. Make sure you have ``pip``::

    sudo yum install python-pip

2. Use ``pip`` to install ``uwsgi``::

    sudo pip install "uwsgi == 2.0.3"


Allow Apache2 to create network connections (SELinux setups only)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    setsebool httpd_can_network_connect true


Configure Apache2 to proxy requests for CLiC Applications
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    sudo cp /usr/local/lib/clic/deploy/apache2/clic.conf /etc/httpd/conf.d/
    sudo service httpd restart


Start the uWSGI Emperor Process
'''''''''''''''''''''''''''''''

::

    sudo uwsgi --ini /usr/local/lib/clic/deploy/uwsgi/emperor.ini


.. NOTE::

   You should probably figure out how to run the uWSGI Emperor service,
   as invoked using the previous command, at boot time.
