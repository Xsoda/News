# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler, admin

class UserList(BaseHandler):
    @admin
    def get(self):
        userlist = self.db.query("select * from usr order by grade desc;")
        self.write(self.serve_template("admin/user.html", **{'userlist': userlist}))

class DelUser(BaseHandler):
    @admin
    def get(self, id):
        if self.db.execute_rowcount("delete from usr where id=%s;", *(id,)):
            self.write('done')
        else:
            self.write('undone')

class EditUser(BaseHandler):
    @admin
    def get(BaseHandler):
        pass

    @admin
    def post(BaseHandler):
        pass
