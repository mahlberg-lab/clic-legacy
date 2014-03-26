"""Setuptools command sub-classes."""

from __future__ import with_statement, absolute_import

import inspect
import os
import re

from os.path import abspath, dirname, exists, expanduser, join

from setuptools import Command
from setuptools.command import develop as _develop
from setuptools.command import install as _install

from cheshire3.exceptions import ConfigFileException
from cheshire3.internal import cheshire3Home, cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.session import Session

from .exceptions import DevelopException, InstallException


class clic_command(Command):
    """Base Class for custom commands."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def apply_config_templates(self):
        "Read config template(s), make subs, write config file(s)."
        global distropath

        def apply_config_tmpl(path):
            "Subroutine to turn templates into configs"
            global distropath
            # Read in template
            with open(path + '.tmpl', 'r') as fh:
                config = fh.read()
            # Make replacements
            config = re.sub('>~/clic/(.*?)</',
                            r'>{0}/\1</'.format(distropath),
                            config
                            )
            # Write finished config file
            with open(path, 'w') as fh:
                fh.write(config)

        # Dickens Database
        apply_config_tmpl(
            join(
                distropath,
                'dbs',
                'dickens',
                'config.xml'
            )
        )

    def run(self):
        raise NotImplementedError()


class develop(_develop.develop, clic_command):

    user_options = _develop.develop.user_options + clic_command.user_options

    def initialize_options(self):
        _develop.develop.initialize_options(self)
        clic_command.initialize_options(self)

    def finalize_options(self):
        _develop.develop.finalize_options(self)
        clic_command.finalize_options(self)

    def install_for_development(self):
        global distropath, server, session
        # Carry out normal procedure
        _develop.develop.install_for_development(self)
        # Use config templates to generate configs
        self.apply_config_templates()
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session,
                                               join(distropath,
                                                    'dbs',
                                                    'dickens',
                                                    'config.xml'
                                                    )
                                               )
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_dickens' is already "
                                   "registered."):
                # Existing install / development install
                raise DevelopException("Package is already installed. To "
                                       "install in 'develop' mode you must "
                                       "first run the 'uninstall' command.")

    def uninstall_link(self):
        global server, session
        # Carry out normal procedure
        _develop.develop.uninstall_link(self)
        # Unregister the database by deleting
        # Cheshire3 database config plugin
        serverDefaultPath = server.get_path(session,
                                            'defaultPath',
                                            cheshire3Root
                                            )
        userSpecificPath = join(expanduser('~'), '.cheshire3-server')
        pluginPath = join('configs', 'databases', 'db_dickens.xml')
        if exists(join(serverDefaultPath, pluginPath)):
            os.remove(join(serverDefaultPath, pluginPath))
        elif exists(os.path.join(userSpecificPath, pluginPath)):
            os.remove(os.path.join(userSpecificPath, pluginPath))
        else:
            server.log_error(session, "No database plugin file")


class install(_install.install, clic_command):

    def run(self):
        # Carry out normal procedure
        _install.install.run(self)
        # Use config templates to generate configs
        self.apply_config_templates()
        # Install Cheshire3 database config plugin
        # Tell the server to register the config file
        try:
            server.register_databaseConfigFile(session,
                                               join(distropath,
                                                    'dbs',
                                                    'dickens',
                                                    'config.xml'
                                                    )
                                               )
        except ConfigFileException as e:
            if e.reason.startswith("Database with id 'db_ead' is already "
                                   "registered."):
                # Existing install / development install
                raise InstallException("Package is already installed. To "
                                       "install you must first run the "
                                       "'uninstall' command.")


# Inspect to find current path
modpath = inspect.getfile(inspect.currentframe())
moddir = dirname(modpath)
distropath = abspath(join(moddir, '..', '..'))
serverConfig = os.path.join(cheshire3Root,
                            'configs',
                            'serverConfig.xml'
                            )
session = Session()
server = SimpleServer(session, serverConfig)
