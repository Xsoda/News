# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler, admin

class Home(BaseHandler):
    
    @admin
    def get(self):
        pass
