Emperor Process
===============

At some point the standard uwsgi process was moved away from as it doesn't allow all that great control of what the process does. The recommended way of running things like this according uwsgi documentation is to use the [emperor process](http://uwsgi-docs.readthedocs.org/en/latest/Emperor.html).

The primary benefits as listed above
1. Whenever an imperial monitor detects a new configuration file, a new uWSGI instance will be spawned with that configuration.
2. Whenever a configuration file is modified (its modification time changed, so touch --no-dereference may be your friend), the corresponding app will be reloaded.
3. Whenever a config file is removed, the corresponding app will be stopped.
4. If the emperor dies, all the vassals die.
5. If a vassal dies for any reason, the emperor will respawn it.

The standard way to do this is with a few configuration files.

```
#emperor.ini

[uwsgi]
emperor = %dapps
vassals-include = %dapps-include.ini
emperor-stats-server = 127.0.0.1:8888
```

```
#apps-include.ini

[uwsgi]
logto = %d/logs/%(vassal_name).log
logfile-chown = true

# Process Management
master = true
processes = 8
```

The process is essentially a master controller that spawns and tears down _vassals_ (essentially uswsgi processes) as they are needed. It's capable of spanning multiple hardware nodes and therefore is well suited to larger projects.

It's also very easy to invoke with

```
sudo uwsgi --ini /cheshire3/clic/deploy/uwsgi/emperor.ini
```

Handily it also watches all the files and the configuration data such that if you _touch_ them it will respawn the process which makes the automatic deployment stuff work really easily.
