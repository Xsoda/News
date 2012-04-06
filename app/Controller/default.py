# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler
from core.web.template import serve_template

class HomeHandler(BaseHandler):
    def get(self):
        print(serve_template("index.html"))
        self.write(serve_template("index.html"))
