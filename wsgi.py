#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, print_function

# Frameworks and core packages
import time
import signal
import os
from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.options import options, define, parse_command_line
from tornado.httpserver import HTTPServer

# settings
from app import settings

# handlers
# from app.handlers import MainHandler

__version__ = "0.1.0-20150101"
__auther__ = ''

# Some configure options
define('host', type=str, default='127.0.0.1')
define('port', type=int, default=5546)
define('cookie_secret', type=str, default="please replace this to your own.")
define('debug', type=bool, default=False)
define('reload', type=bool, default=True)
define('xsrf', type=bool, default=True)
define('config', type=str, default='')

# static and templates path defintion
static_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'app/static')
template_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'app/templates')


server = None
loop = None


def stop_loop():
    loop.stop()


def signal_handler_child_callback():
    server.stop()
    # allow to finish processing current requests
    loop.add_timeout(time.time() + 30, stop_loop)


def signal_handler(signum, frame):
    global loop
    global server
    if loop:
        # this is child process, will restrict incoming connections and stop
        # ioloop after delay
        loop.add_callback(signal_handler_child_callback)
    else:
        # this is master process, should restrict new incomming connections
        # and send signal to child processes
        server.stop()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        os.killpg(0, signal.SIGTERM)


def get_app(debug=False, xsrf=True):
    parse_command_line()
    app_settings = {
        # framework settings
        'debug': debug,
        'static_path': static_path,
        'template_path': template_path,
        'login_url': '/login/',
        'reload': options.reload,
        'cookie_secret': options.cookie_secret,
        'xsrf_cookies': xsrf,
    }

    routers = [

    ]
    if debug is True:
        routers.append((r'/static/(.*)', StaticFileHandler))
    app = Application(routers, **app_settings)
    return app

if __name__ == "__main__":
    parse_command_line()
    application = get_app(options.debug, options.xsrf)
    try:
        print('serving on http://' + options.host + ':' + str(options.port))
        if options.debug:
            application.listen(options.port, options.host)
            IOLoop.instance().start()
        else:
            signal.signal(signal.SIGTERM, signal_handler)
            server = HTTPServer(application)
            server.bind(options.port, options.host)
            server.start(0)
            ioloop = IOLoop.instance()
            ioloop.start()
    except KeyboardInterrupt:
        print('Recived exit signal, Exiting...')
