Settings
========

There are a few settings that can be set project-wide. The default settings
file that is used is ``settings.py``. 

Using local settings
--------------------

NB: This is only for developers.

If one is developing in a local development environment of which the directory 
structure differs from the production setup (for instance, when using a virtual 
environment rather than a virtualbox), it is possible to define local settings 
in a ``local_settings.py`` file. To make these changes effective one needs to 
set an OS environment variable ``CLIC_SETTINGS`` to ``local``::

    export CLIC_SETTINGS=local

If that environment 
variable is set, any settings that have been declared in ``local_settings.py`` 
will overwrite the default ``settings.py`` settings. 

In order to avoid setting the ``CLIC_SETTINGS`` environment variable each time
one opens the project locally, one can set it automatically each time the 
virtual environment is activated. This is done by adding the export command above
to your virtual environment `bin/postactivate` file.

Python
------

Currently the only setting that is used is::

    DATA_DIR 

which specifies where run.py can find the data it wants to 
feed to the database.

Other settings in the future could include::

    CACHE_DIR
    CACHE_LOCK

in the api.py file. 



XML configurations
==================

The most important config files are all in XML. These are
currently still hard-coded. 
