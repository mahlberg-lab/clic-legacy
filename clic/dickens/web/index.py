"""CLiC Dickens Search Application"""

from __future__ import absolute_import

import sys

from mod_python_wsgi.wrap import ModPythonWSGIApp

from clic.deploy.utils import WSGIAppArgumentParser
from clic.dickens.web.dickensHandler import handler


def main(argv=None):
    """Start up a simple app server to serve the application."""
    global argparser, application
    global application
    import paste.httpserver
    from paste.urlmap import URLMap
    from paste.urlparser import make_pkg_resources
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    urlmap = URLMap(make_pkg_resources(None, 'clic', 'www/dickens'))
    urlmap['/'] = application
    paste.httpserver.serve(urlmap,
                           host=args.hostname,
                           port=args.port,
                           )


application = ModPythonWSGIApp(handler)

# Set up argument parser
argparser = WSGIAppArgumentParser(
    conflict_handler='resolve',
    description=__doc__.splitlines()[0]
)

if __name__ == '__main__':
    sys.exit(main())

