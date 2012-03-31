#*-*coding: utf-8*-*
__author__='Xsoda'

import tornado.escape
import uuid
import time
import core.db
import tornado.web
import functools

from tornado.web import HTTPError

class Session:

    def __init__(self, session_id=None, store=None, args={}):
        if store == 'Postgres':
            pass
        else:
            self.store = Session_Store_StaticClass()

        self.time = 86400
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = self._generate_session_id()

    def _generate_session_id(cls):
        return str(uuid.uuid4())

    def id(self):
        return self.session_id

    def set(self, key, value):
        self.store.set(self.session_id, key, value, self.time)

    def get(self):
        return self.store.get(self.session_id, key)

    def delete(self, key):
        self.store.delete(self.session_id, key)

    def clear(self, key):
        self.store.clear(self.session_id)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __len__(self):
        return len(self.data.keys())

    def __str__(self):
        return self.data

    def keys(self):
        return self.data.keys()
    

class Session_Store_StaticClass:
    
    _Data = {}
    
    def get_session(self, session_id):
        if session_id in Session._Data:
            return Session._Data[session_id]
        return {}

    def set(self, session_id, key, value, time=0):
        session = self.get_session(session_id)
        session[key] = value
        Session._Data[session_id] = session

    def get(self, session_id, key):
        session = self.get_session(session_id)
        if key in session:
            return session[key]
        return {}

    def delete(self, session_id, key):
        session = self.get_session(session_id)
        if key in session:
            del session[key]
            Session._Data[session_id] = session

    def clear(self, session_id):
        if session_id in Session._Data:
            del Session._Data[session_id]
        

class RequestHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._start_time = time.time()
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
    def session(self):
        if hasattr(self, '_session'):
            return self._session

        if self.get_secure_cookie('PYSESSID'):
            self._session = Session(self.get_secure_cookie('PYSESSID'), self.settings['session']['store'], self.settings['session']['args'])
        else:
            self._session = Session(False, self.settings['session']['store'],self.settings['session']['args'])
            self.set_secure_cookie('PYSESSID', self._session.id())

        return self._session

    def error(self, **args):
        args['url'] = args['url'] if 'url' in args else self.request.path
        self.render("error.html", **args)
        self._finished = True
        return

    def get_session(self, key):
        return self.session().get(key)

    def set_session(self, key, val):
        self.session().set(key, val)

    # 访问被拒绝时的错误处理函数
    def _on_access_denied(self):
        self.error(msg="403 禁止访问", url='/login')

    def set_acl_current_user(self, info, roles=[]):
        user_info = info
        user_info['roles'] = roles
        self.session().set('current_user', user_info)

    def acl_current_user(self):
        current_user = self.session().get('current_user')
        if not current_user:
            return {}
        return current_user

    def clear_acl_current_user(self):
        self.session().delete('current_user')

    def request_time(self):
        return time.time() - self._start_time

