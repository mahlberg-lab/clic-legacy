Requirements
============

To install CLiC get all the dependencies it needs. These are best installed
inside of a virtual environment. 

The requirements in the production.txt, testing.txt and dev.txt files import the base.txt file. Any project wide dependencies should go in the base.txt file. Ideally, the production.txt file is empty.

To install these requirements, run ``pip install`` for the respective file. For instance, to install the development dependencies, run::

     pip install -r dev.txt

The flag ``-r`` allows one to point at a file that contains the dependencies. To see which packages were installed, run::

     pip freeze


Note to devs
------------

* The requirements are specified with an exact release number.
* Any new dependencies that are manually installed should be added to the requirements. This is not needed for dependencies of dependencies. 
* To check whether any packages are outdated, one can run ``pip list --outdated``
* To write all dependencies to a file, one can run ``pip freeze > some-filename.txt``
