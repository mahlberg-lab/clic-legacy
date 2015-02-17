CLiC Project
============

Cheshire3 databases and applications for the CLiC Project.

Run
---

Start a web-server to make the interface available locally::

:: sudo su -c "uwsgi --http :8080 --wsgi-file clic/dickens/web/flask/api.py --callable app" cheshire