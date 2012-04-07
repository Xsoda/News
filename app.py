# *-* coding: utf-8 *-*
#! /usr/bin/env python

import os.path
import re
import core.db.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import app.controller
from app.controller import * 

from tornado.options import define, options

define("port", default=9000, help="run on the given port", type=int)
define("pg_host", default="127.0.0.1:5432", help="database host")
define("pg_database", default="news", help="database name")
define("pg_user", default="postgres", help="database user")
define("pg_password", default="1989ii24", help="database password")
define("template_directory", default="app/view", help="default mako template directory")
define("mako_moudle_dir", default="app/view/mako_moudle", help="default mako complie template directory")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            title = "PPTM News",
            template_path = os.path.join(os.path.dirname(__file__), "app/view/"),
            static_path = os.path.join(os.path.dirname(__file__), "app/static/"),
            xsrf_cookies = True,
            cookie_secret = "760f802ae2ea1ca7120b1fee4e9aa16e3ea53698/Vo=",
            login_url = "/auth/login",
        )

        handlers = [
            (r"/", app.controller.HomeHandler.HomeHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = core.db.database.Connection(
            host = options.pg_host, database = options.pg_database,
            user = options.pg_user, password = options.pg_password)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop=io_loop, check_time=500)
    io_loop.start()
    
if __name__ == "__main__":
    main()
