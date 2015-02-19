Requirements
============

To install CLiC get all the dependencies it needs. These are best installed
inside of a virtual environment. 

The requirements in the production.txt, testing.txt and dev.txt files import the base.txt file. Any project wide dependencies should go in the base.txt file. Ideally, the production.txt file is empty.

To install these requirements, run a `pip install` for the respective file. For instance, to install the development dependencies, run:

     pip install dev.txt

Note to devs: the requirements are specified with an exact release number.
