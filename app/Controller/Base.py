import tornado.web
from mako.template import Template
from mako.lookup import TemplateLookup

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return self.db.get("Select * from usr where id = %s", int(user_id))

    def template_exists(self, template_name):
        if self.__template_exists_cache.get(template_name, None):
            print("found in cache: " + template_name)
            return True
        lookup = self._get_template_lookup()
        try:
            new_template = lookup.get_template(template_name)
            if new_template:
                self.__template_exists_cache[template_name] = True
                return True
        except Exception as detail:
            print("run-time error in BaseRequest::template_exists - ", detail)
            self.__template_exists_cache[template_name] = False

    def _get_template_lookup(self, extra_imports=None):
        if not self.lookup:
            self.lookup = TemplateLookup(directories=[], module_directory=,output_encoding='utf-8',encoding_errors=replace)
        return self.lookup

    def serve_template(self, template_name, **kwargs):
        if template_exists(template_name):
            template = __template_exists_cache[template_name]
            return template.render(**kwargs)
        else:
            lookup = self._get_template_lookup()
            template = lookup.get_template(template_name)
            return template.render(**kwargs)
