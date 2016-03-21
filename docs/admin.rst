CLiC for administrators
=======================


For the deployment of CLiC we heavily rely on Docker. This has several benefits:
it packages all the dependencies of CLiC together in a simple image and it makes
a deployment much faster and possible on many different platforms. 

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
    sudo vimsu /etc/default/ufw

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

    sudo docker login  # (you may need login details)
    sudo docker pull jdejoode/clic


Step 4: Get the indexes and stores
##################################

``TODO``


Step 5: Run the Docker container
################################

The ``path-to`` elements in the following snippets need to be replaced with
the actual path to your indexes, stores, configs, and code.

.. code:: bash

  sudo docker run -d -p 80:80 -v
  /home/path-to-/indexes:/clic-project/clic/dbs/dickens/indexes -v
  /home/path-to-/stores:/clic-project/clic/dbs/dickens/stores --name
  clic jdejoode/clic:latest

What the above command does:

    - Run a docker container called jdejoode/clic with the latest tag
      as the exact version
    - The key parts are the ‘run’ and the image name
      ‘jdejoode/clic:latest’
    - The –d is used to run docker as a daemon (to keep it running,
      otherwise it only runs a single command)
    - -p 80:80 tells the host to forward port 80 to 8080
    - -v host:docker mounts two different folders (the indexes and the stores)
      which are essential to clic.

Or if you want to be able to update and release new code, you can mount the code
and the configs (the config file needs to be the one from clic-docker):

.. code:: bash

  docker run -d --name clic-code13 -v
  /Users/path-to-clic-code/clic:/clic-project/clic -v
  /Users/path-to-clic-indexes/indexes:/clic-project/clic/dbs/dickens/indexes -v
  /Users/path-to-clic-stores/stores:/clic-project/clic/dbs/dickens/stores -v
  /Users/path-to-clic-config/config.xml:/clic-project/clic/dbs/dickens/config.xml
  -p 80:8080 -p 5000:5000 jdejoode/clic:latest


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



Installing CLiC on your own computer
------------------------------------

Because of the CLiC is released as a Docker image, you can also install CLiC on
your own computer (Mac, Windows, or Linux) by simply installing Docker and
following the system-specific install instructions in the Docker docs.



Releasing a new version
-----------------------

There are several steps that need to be taken for a new release.

    1.     Prepare the release on github

      a.     Update CHANGELOG.rst

      b.     Merge branches into develop and develop into master

      c.     Tag master with the latest version

      d.     Git push && git push --tags

    2.     Update the date in the Dockerfile (add sth random if you have too
    more than one release on a day, the purpose is to invalidate the Docker
    image cache)

      a.     RUN git clone -b master
      https://github.com/CentreForCorpusResearch/clic.git && echo "2015-10-23"

      b.     Docker build –t jdejoode/clic:latest .

                        i.         To check build
  on local first:

                       ii.         docker run -d
  --name clic-debug -v
  /Users/johan/Data/clic/indexes:/clic-project/clic/dbs/dickens/indexes -v
  /Users/johan/Data/clic/stores:/clic-project/clic/dbs/dickens/stores -P
  jdejoode/clic:latest   # -P needs to be before image name

                       iii.     on mac: docker-machine env default

                       iv.     on mac: docker port clic-debug

                        v.         then visit the
  localhost on the right port: for instance, http://192.168.99.100:32770/

      c.      Docker login

      d.     Docker push jdejoode/clic:latest

  3.     On the server you want to push to:

      a.     Sudo docker login

      b.     Sudo docker pull jdejoode/clic:latest

      c.      Sudo docker ps

      d.     Sudo docker stop NAMEOFTHERUNNINGCONTAINER (stop the running
      container, make sure you do not lose data!)

      e.     sudo docker run -d -p 80:8080 -v /tmp:/tmp -v
      /home/clicman/indexes:/clic-project/clic/dbs/dickens/indexes -v
      /home/clicman/stores:/clic-project/clic/dbs/dickens/stores --name clic8
      jdejoode/clic:latest

  4.     Run the tests

    a.     BASE\_URL='http://live/' py.test main.py  (in
    clic/tests/functional tests/)
