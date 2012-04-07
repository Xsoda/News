# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.write(self.serve_template("test.html",**{'name':'Xsoda'}))
