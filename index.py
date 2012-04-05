# *-* coding: utf-8 *-*
#! /usr/bin/env python

import os.path
import re
import core.db.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=9000, help="run on the given port", type=int)
define("pg_host", default="127.0.0.1:5432", help="database host")
define("pg_database", default="news", help="database name")
define("pg_user", default="postgres", help="database user")
define("pg_password", default="xxxxxxxx", help="database password")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            title = "PPTMNews",
            template_path = os.path.join(os.path.dirname(__file__), "view/"),
            static_path = os.path.join(os.path.dirname(__file__), "static/"),
            xsrf_cookies = True,
            cookie_secret = "/Vo=",
            login_url = "/auth/login",
        )

        handlers = [
            (r"/", app.controller.HomeHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = core.db.database.Connection(
            host = options.pg_host, database = options.pg_database,
            user = options.pg_user, password = options.pg_password)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_current_user("user")
        if not user_id:
            return None
        return self.db.get("select * from usr where id = %s", int(user_id))

