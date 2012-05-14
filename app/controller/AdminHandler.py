# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

import time
import random
import string
from app.controller.Base import BaseHandler, admin
from core.web.helpers import Gravatar

gravatar = Gravatar(size=140, rating='g', default=None, force_default=False, force_lower=True)

class Home(BaseHandler):
    
    @admin
    def get(self):
        category = self.db.query("select * from category;")
        self.write(self.serve_template("admin/news.html", **{'category': category, 'xsrf': self.xsrf_form_html()}))
        self.finish()

class ImgPost(BaseHandler):

    def check_xsrf_cookie(self):        # 当上传图片时禁用 xsrf
        pass
    
    @admin
    def post(self):
        if self.request.files:
            f =  self.request.files['myfile'][0]
            original_fname = f['filename']
            final_fname = str(int(time.time())) + ''.join(random.choice(string.ascii_lowercase) for x in range(4)) +  '.'+ original_fname.split('.').pop()
            output_file = open("app/static/uploads/" + final_fname, 'wb')
            output_file.write(f['body'])
            output_file.close()
            self.write("/static/uploads/" + final_fname)
        self.finish()

class GetAdmin(BaseHandler):
    @admin
    def get(self):
        self.write('<img height="50" src={gravatar} onerror="this.src=\'../static/image/default.png\'"'
                   '></img>{name} & <a href="/auth/logout">注销</a>'.format(**{'gravatar': gravatar(self.current_user['email']),
                                                                               'name': self.current_user['name']}))
        
