import tornado.web
from tornado.options import define, options
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback
from core.session.session import RedisSession
import markdown
from docutils.core import publish_parts
import re

class BaseHandler(tornado.web.RequestHandler):

    def PyStrEscape(self, html):
        return html.replace('"', '&quot;').replace("'", "&acute;")

    def JsEscape(self, html):
        pattern = re.compile(r"<\s*script(?:.|\s)*?(?:/\s*>|<\s*/script\s*>)")
        iterator = pattern.finditer(html)
        result = []
        index = 0
        for match in iterator:
            start, end = match.span()
            if start > index:
                result.append(html[index : start - 1])
            js = html[start:end].replace('<', '&lt;').replace('>', '&gt;')
            result.append(js)
            index = end + 1
        else:
            html = ''.join(result) if result else html
        return html
    
    @property
    def db(self):
        return self.application.db
   
    def get_current_user(self):
        return self.session['user'] if self.session and 'user' in self.session else None

    @property
    def markdown(self):
        if hasattr(self, '_markdown'):
            return self._markdown.convert
        else:
            self._markdown = markdown.Markdown()
        return self._markdown.convert

    def reStructuredText(self, rst):
        return publish_parts(rst, writer_name="html")['body']

    def DocParise(self, doc, source):
        source = "该新闻没有任何内容\n=========================\n该新闻没有任何内容" if source is None else source
        if doc == 'html':
            return source
        elif doc == 'Markdown':
            return self.markdown(source)
        elif doc == 'reStructuredText':
            return self.reStructuredText(source)
        return 'error'
    
    def isAdmin(self):
        if hasattr(self, 'current_user'):
            if self.current_user and int(self.current_user['grade']) == 1:
                return True
        return False

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            sessionid = self.get_secure_cookie('sid')
            self._session = RedisSession(self.application.session_store, sessionid, expires_days=options.expires_days)
            if not sessionid:
                self.set_secure_cookie('sid', self._session.sessionid, expires_days=options.expires_days)
        return self._session
    
    def template_exists(self, template_name):
        self._template_exists_cache = {}
        if self._template_exists_cache.get(template_name, None):
            print("found in cache: " + template_name)
            return self._template_exists_cache[template_name]
        lookup = self._get_template_lookup()
        try:
            new_template = lookup.get_template(template_name)
            if new_template:
                self._template_exists_cache[template_name] = new_template   
                return self._template_exists_cache[template_name]
        except Exception as detail:
            print("run-time error in BaseRequest::template_exists - ", detail)
            self._template_exists_cache[template_name] = None

    def _get_template_lookup(self, extra_imports=None):
        self.lookup = None
        if not self.lookup:
            self.lookup = TemplateLookup(directories=[options.template_directory], module_directory=options.mako_moudle_dir, input_encoding="utf-8", output_encoding='utf-8', encoding_errors="replace")
        return self.lookup

    def serve_template(self, template_name, **kwargs):
        try:
            if self.template_exists(template_name):
               template = self._template_exists_cache[template_name]
               return template.render(**kwargs)
            else:
              lookup = self._get_template_lookup()
              template = lookup.get_template(template_name)
              return template.render(**kwargs)
        except:
            traceback = RichTraceback()
            for (filename, lineno, function, line) in traceback.traceback:
                print("File %s, line %s, in %s" % (filename, lineno, function))
                print(line, "\n")
            print("%s: %s" % (str(traceback.error.__class__.__name__), traceback.error))
                  
class authenticated(object):

    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        def login_wrapper(_self, *args, **kwargs):
            userinfo = _self.current_user
            if userinfo:
                return method(_self, *args, **kwargs)
            return _self.redirect(_self.get_login_url())
        
        def admin_wrapper(_self, *args, **kwargs):
            userinfo = _self.current_user
            if userinfo and int(userinfo['grade']) == 1:
                return method(_self, *args, **kwargs)
            return _self.redirect(_self.get_login_url())

        if self.role == "admin":
            return admin_wrapper
        elif self.role == "user":       # user 角色仅仅是简单的登录验证， 所以即使当前登录的是 admin 权限，也可以通过验证
            return login_wrapper
        else:
            print("unkown role")
