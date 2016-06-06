CLiC for administrators
=======================


For the deployment of CLiC we rely on Docker. This has several benefits:
it packages all the dependencies of CLiC together in a simple image and it makes
a deployment much faster and platform-independent.

Installing CLiC on your own server
----------------------------------

Step 1: Install Docker on a vanilla Ubuntu server
#################################################
 
.. code:: bash

    # Install Docker in a way that can easily be upgraded
    sudo apt-get update

    sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys
    58118e89f3a912897c070adbf76221572c52609d

    # open the /etc/apt/sources.list.d/docker.list file in your favorite
    editor. if the file doesn’t exist, create it. and add:

      # this is not a command, but something that needs to be pasted in the
      file opened
      
      deb https://apt.dockerproject.org/repo ubuntu-trusty main 

    sudo apt-get update

    # verify that apt is pulling from the right repository.

    sudo apt-cache policy docker-engine

    sudo apt-get install linux-image-generic-lts-trusty

    # you need to reboot, this can cause some issues where the firewall
    settings would not be saved, this was solved by loading the firewall
    explicitly at the restart

    sudo reboot

    sudo apt-get update

    sudo apt-get install docker-engine

    sudo docker run hello-world


Step 2: Configure Docker
########################

.. code:: bash

    # set UFW’s forwarding policy appropriately.
    # Open /etc/default/ufw file for editing.
    sudo vim /etc/default/ufw

    # Set the DEFAULT\_FORWARD\_POLICY policy to:
    DEFAULT\_FORWARD\_POLICY="ACCEPT"

    sudo ufw reload

    #TODO check if this is persistent

    # Allow incoming connections on the Docker port.
    $ sudo ufw allow 2375/tcp 

    # Configure Docker to start on boot
    # DOCS SAY $ sudo systemctl enable docker
    # but I think:

    sudo update-rc.d docker defaults


Excursus: Quick Docker command guide
####################################

You might have to prepend ``sudo`` to the commands below, depending on your
environment.

.. code:: bash

    # is docker installed
    docker info

    # activate docker
    docker-machine start default
    eval "$(docker-machine env default)"

    # to find localhost ping
    docker-machine env default

    # to build
    cd ~/ImagesDocker/clic-docker/
    docker build -t jdejoode/clic:v0 .

    # list images
    docker images

    # run a docker image
    docker run -d -P -i -t --name apache11 jdejoode/clic:v0 docker ps

    # find info on container
    docker port apache11
    docker logs a5a665d32

    # for live updates a la Flask
    docker logs –f a6516a51sd f651

    # stop all docker containers
    docker stop $(docker ps -a -q)

    # remove them
    docker rm $(docker ps -a -\ **q**\ )

    # ssh into container
    docker exec -i -t fbd8112 bash

    # command on actual deploy is slightly different for caching and
    rounting purposes:
    # -v /path/on/host:/path/in/container
    docker run -p 80:8080 –v /tmp/cache:/tmp/cache …

    docker run -d -P --name clic2 -v
    /bin:/clic-project/clic/dbs/dickens/indexes jdejoode/clic:v0

    # to see what processes run in the container
    docker top clic0

    # remove untagged images
    docker rmi $(docker images \| grep "^<none>" \| awk '{print $3}')

    # deploy
    # on macbook
    # https://docs.docker.com/docker-hub/repos/
    docker login
    docker push jdejoode/clic:latest


    # You can also bind Docker containers to specific ports using the-p flag,
    for example:
    $ docker run -d -p 80:5000 training/webapp python app.py


Step 3: Get CLiC's Docker image
###############################
     
.. code:: bash

    # you can upload the Docker image found on the shared drive
    `mahlbema-01` in the folder `CLiC Live Server Data and Image`
    
    Do load the image on the server, run:
    
    docker load -i path-to-uploaded-CliCLive.tar 
    
    For instance:
    
    sudo docker load -i CLiCLive.tar
    

Step 4: Get the indexes, stores, and code
#########################################

The indexes can be downloaded from the same shared drive (`mahlbema-01`).
They need to be uploaded to the server as they need to be included in the 
Docker container as volumes when initialising the Docker container. 

.. code:: bash

    git clone https://github.com/CentreForCorpusResearch/clic
    

Step 5: Run the Docker container
################################

The ``path-to`` elements in the following snippets need to be replaced with
the actual path to your indexes, stores, configs, and code.

.. code:: bash

  sudo docker run -d -p 80:8080 -p 5000:5000 
  -v /home/clicman/clic:/clic-project/clic 
  -v /home/clicman/indexes:/clic-project/clic/dbs/dickens/indexes 
  -v /home/clicman/stores:/clic-project/clic/dbs/dickens/stores 
  -v /home/clicman/db_annotation_2016_05_10_at_12_00.tar:/clic-project/clic/db_annotation.tar 
  -v /home/clicman/config.xml:/clic-project/clic/dbs/dickens/config.xml 
  -v /home/clicman/textfiles:/clic-project/clic/clic/textfiles 
  --name clic jdejoode/clic:latest

What the above command does:

    - Run the CLiC Docker container called with the latest tag
      as the exact version
    - The –d is used to run docker as a daemon (to keep it running,
      otherwise it only runs a single command)
    - -p 80:8080 tells the host to forward port 80 to 8080
    - -v host:docker mounts two different folders (the indexes and the stores)
      which are essential to clic. These are not included in the Docker image as
      they are volatile and as they are too big.

This enables you to update and release new code that does not change the database
as the code and the configs are mounted.

Get the database up and running:

.. code:: bash

  # move into the container
  docker exec -it clic bash
  
  # run the following commands
  dropdb db_annotation
  dropuser clic-dickens
  sudo -u postgres createuser -P -d -r -s clic-dickens
  createdb -O clic-dickens db_annotation --password
  # db_annotation.tar is the db.tar that was mounted earlier
  pg_restore --dbname=db_annotation --verbose /clic-project/clic/db_annotation.tar 
  
  # update to the latest, more advanced caching framework
  pip install --upgrade Beaker pandas

  # restart uwsgi and postgres
  supervisorctl restart all
  
This should get CLiC up and running on your server/computer. Make sure to check 
whether the forms actually work before considering the installation a success.

There are functional tests in clic/tests/functional/main.py. Read that document 
for more information. 

Before destroying a container, on has to export the postgres database. For instance:

.. code:: bash

  pg_dump -U clic-dickens -h localhost -W -F t db_annotation > /clic-project/clic/db_annotation.tar

Enjoy, unless ...
#################

To troubleshoot the container:

.. code:: bash

  # Is the container running?
  sudo docker ps

  # Are the right processes running on the container?
  sudo docker top clic  # (where clic is the name of the container)

  # Did the volumes mount correctly?
  Exec into the clic container to check manually whether the volumes are mounted

  # What do the logs say?
  sudo docker logs afcb70

  # What services are listening on what ports?
  sudo netstat –peanut

  # Do you get "ACCEPT: iptables: No chain/target/match by that name" 
  sudo service docker restart
  
  # In very rare cases, a container might go down without prior notice. In that case
  # check whether it is up:
  sudo docker ps
  # if it is not up restart it
  sudo docker start clic (where clic is the container name)


Installing CLiC on your own computer
------------------------------------

Because of the CLiC is released as a Docker image, you can also install CLiC on
your own computer (Mac, Windows, or Linux) by simply installing Docker and
following the system-specific install instructions in the Docker docs.


Run the tests
-------------

To run the tests:

.. code:: bash

    BASE_URL='http://live/' py.test main.py  (in
    clic/tests/functional tests/)
