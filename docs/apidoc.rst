CLiC for developers
===================

Cheshire3
---------

The data-model
##############


CLiC Concordance
----------------

.. automodule:: concordance
   :members:

CLiC Clusters
-------------

.. automodule:: clusters
   :members:

CLiC Keywords
-------------

.. automodule:: keywords
   :members:

CLiC Chapter Repository
-----------------------

.. automodule:: chapter_repository
   :members:

CLiC KWICgrouper
----------------

.. automodule:: kwicgrouper
   :members:

CLiC Normalizer
---------------

.. automodule:: normalizer
   :members:

CLiC Query Builder
------------------

.. automodule:: querybuilder
   :members:

CLiC Web app
-------------

Index
#####

.. automodule:: web.index

API
#####

.. automodule:: web.api

Models
######

.. automodule:: web.models
   :members:


How to run the local development server?::
----------------------------------------


    ~/projects/clic/clic/clic/web$ PYTHONPATH=~/projects/clic/clic python manage.py runserver

How to run new indexes?::
-----------------------

    ~/projects/clic/clic/dbs/dickens/indexes$ CLIC_SETTINGS=local PYTHONPATH=~/projects/clic/clic python run.py --ntc
    ~/projects/clic/clic/dbs/dickens/indexes$ CLIC_SETTINGS=local PYTHONPATH=~/projects/clic/clic python run.py --dickens




